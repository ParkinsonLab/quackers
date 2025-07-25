#!/usr/bin/env python3
"""
Maximum Performance Bin Refinement Script - Quiet Version
"""

import os
import sys
import subprocess
import multiprocessing
import concurrent.futures
from pathlib import Path
import shutil
import argparse
import time
import psutil


def setup_bins(source_dir, target_dir, min_size=100000):
    """Setup bin directory with symlinks."""
    target_path = Path(target_dir)
    if target_path.exists():
        shutil.rmtree(target_path)
    target_path.mkdir(exist_ok=True)
    
    source_path = Path(source_dir)
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")
    
    count = 0
    for fa_file in source_path.glob("*.fa"):
        if fa_file.stat().st_size >= min_size:
            (target_path / fa_file.name).symlink_to(fa_file.resolve())
            count += 1
    
    return count


def run_refinement_job(job_info):
    """Run a single refinement job."""
    name, output_dir, cmd_args, threads, memory_gb = job_info
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Setup environment
    env = os.environ.copy()
    env.update({
        'OMP_NUM_THREADS': str(threads),
        'NUMEXPR_NUM_THREADS': str(threads),
        'MKL_NUM_THREADS': str(threads),
        'OPENBLAS_NUM_THREADS': str(threads),
        'CHECKM_THREADS': str(threads),
        'HMMER_NCPU': str(threads),
        'BLAST_NUM_THREADS': str(threads),
        'JAVA_OPTS': f'-Xmx{int(memory_gb)}g -Xms{int(memory_gb//2)}g',
        'OMP_PROC_BIND': 'true',
        'OMP_PLACES': 'cores',
        'PYTHONUNBUFFERED': '1',
    })
    
    start_time = time.time()
    
    try:
        # Run metaWRAP quietly
        result = subprocess.run([
            'python3', 
            '/quackers_tools/metaWRAP-1.3/bin/metawrap-scripts/binning_refiner.py'
        ] + cmd_args, 
        env=env,
        capture_output=True,
        text=True,
        cwd=os.getcwd(),
        timeout=7200  # 2 hour timeout
        )
        
        elapsed_time = time.time() - start_time
        
        if result.returncode != 0:
            return name, 0, elapsed_time, f"Failed (exit code {result.returncode})"
        
    except subprocess.TimeoutExpired:
        return name, 0, time.time() - start_time, "Timeout"
    except Exception as e:
        return name, 0, time.time() - start_time, f"Error: {e}"
    
    # Count results
    refined_dir = Path(output_dir) / "Refined"
    if refined_dir.exists():
        all_files = list(refined_dir.glob("*.fa")) + list(refined_dir.glob("*.fasta"))
        if all_files:
            total_size = sum(f.stat().st_size for f in all_files) / (1024 * 1024)  # MB
            return name, len(all_files), elapsed_time, f"{total_size:.1f}MB"
    
    return name, 0, elapsed_time, "No output"


def run_parallel_refinements(bins1_count, bins2_count, bins3_count, threads, memory_gb):
    """Run refinements in parallel."""
    
    # Prepare jobs
    jobs = []
    if bins1_count > 0 and bins2_count > 0:
        jobs.append(("A+B", "Refined_AB", ["-1", "bins1", "-2", "bins2", "-o", "Refined_AB", "-ms", "1000"]))
    if bins2_count > 0 and bins3_count > 0:
        jobs.append(("B+C", "Refined_BC", ["-1", "bins2", "-2", "bins3", "-o", "Refined_BC", "-ms", "1000"]))
    if bins1_count > 0 and bins3_count > 0:
        jobs.append(("A+C", "Refined_AC", ["-1", "bins1", "-2", "bins3", "-o", "Refined_AC", "-ms", "1000"]))
    if bins1_count > 0 and bins2_count > 0 and bins3_count > 0:
        jobs.append(("A+B+C", "Refined_ABC", ["-1", "bins1", "-2", "bins2", "-3", "bins3", "-o", "Refined_ABC", "-ms", "1000"]))
    
    if not jobs:
        return 0
    
    # Resource allocation
    threads_per_job = max(4, threads // len(jobs))
    memory_per_job = memory_gb / len(jobs)
    
    print(f"Running {len(jobs)} parallel refinements ({threads_per_job} threads each)")
    print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Add resource info to jobs
    job_configs = [(name, output_dir, args, threads_per_job, memory_per_job) 
                   for name, output_dir, args in jobs]
    
    # Execute in parallel
    overall_start = time.time()
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(jobs)) as executor:
        futures = {executor.submit(run_refinement_job, job): job[0] for job in job_configs}
        
        for future in concurrent.futures.as_completed(futures):
            current_time = time.time()
            elapsed_overall = current_time - overall_start
            
            result = future.result()
            results.append(result)
            name, count, job_time, info = result
            
            if count > 0:
                print(f"✅ {name}: {count} bins ({info}) - job: {job_time:.0f}s, total elapsed: {elapsed_overall/60:.1f}m")
            else:
                print(f"❌ {name}: {info} - total elapsed: {elapsed_overall/60:.1f}m")
    
    overall_time = time.time() - overall_start
    total_bins = sum(r[1] for r in results)
    
    print(f"\n🏁 All jobs completed!")
    print(f"   Total runtime: {overall_time/60:.1f} minutes ({overall_time:.0f} seconds)")
    print(f"   Total refined bins: {total_bins}")
    print(f"   Average rate: {total_bins/overall_time:.2f} bins/second")
    print(f"   Finished at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    return total_bins


def main():
    parser = argparse.ArgumentParser(description="High-Performance Bin Refinement")
    parser.add_argument("-1", "--bins1", required=True, help="First bin directory")
    parser.add_argument("-2", "--bins2", required=True, help="Second bin directory")
    parser.add_argument("-3", "--bins3", help="Third bin directory")
    parser.add_argument("-o", "--output", required=True, help="Output directory")
    parser.add_argument("--threads", "-t", type=int, default=multiprocessing.cpu_count())
    parser.add_argument("--memory", "-m", type=float)
    parser.add_argument("--min-size", type=int, default=100000)
    
    args = parser.parse_args()
    
    # Calculate memory
    if args.memory is None:
        try:
            args.memory = psutil.virtual_memory().total / (1024**3) * 0.8
        except:
            args.memory = 32.0
    
    print(f"🚀 Bin Refinement: {args.threads} threads, {args.memory:.0f}GB RAM")
    
    try:
        # Resolve paths
        original_cwd = Path.cwd()
        bins1_path = Path(args.bins1).resolve() if Path(args.bins1).is_absolute() else (original_cwd / args.bins1).resolve()
        bins2_path = Path(args.bins2).resolve() if Path(args.bins2).is_absolute() else (original_cwd / args.bins2).resolve()
        bins3_path = None
        if args.bins3:
            bins3_path = Path(args.bins3).resolve() if Path(args.bins3).is_absolute() else (original_cwd / args.bins3).resolve()
        
        output_path = Path(args.output).resolve() if Path(args.output).is_absolute() else (original_cwd / args.output).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
        os.chdir(output_path)
        
        # Setup bins
        bins1_count = setup_bins(str(bins1_path), "bins1", args.min_size)
        bins2_count = setup_bins(str(bins2_path), "bins2", args.min_size)
        bins3_count = 0
        if bins3_path:
            bins3_count = setup_bins(str(bins3_path), "bins3", args.min_size)
        
        print(f"Input bins: {bins1_count + bins2_count + bins3_count} total")
        
        if bins1_count == 0 and bins2_count == 0 and bins3_count == 0:
            print("❌ No bins meet size requirements")
            sys.exit(1)
        
        # Run refinements
        total_refined = run_parallel_refinements(bins1_count, bins2_count, bins3_count, args.threads, args.memory)
        
        # Cleanup
        for temp_dir in ["bins1", "bins2", "bins3"]:
            temp_path = Path(temp_dir)
            if temp_path.exists():
                shutil.rmtree(temp_path)
        
        # Results
        if total_refined > 0:
            print(f"\n🎉 Results in: {output_path}")
            for result_dir in ["Refined_AB", "Refined_BC", "Refined_AC", "Refined_ABC"]:
                result_path = output_path / result_dir / "Refined"
                if result_path.exists():
                    count = len(list(result_path.glob("*.fa")) + list(result_path.glob("*.fasta")))
                    if count > 0:
                        print(f"   {result_dir}: {count} bins")
        
        sys.exit(0 if total_refined > 0 else 1)
        
    except Exception as e:
        print(f"💥 ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()