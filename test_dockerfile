# Optimized Dockerfile for Quackers Pipeline
# Version 3.1.0 - Ubuntu 24.04 with Python 2.7 from source

FROM ubuntu:24.04

# Set environment variables early
ENV TZ=America/Toronto \
    DEBIAN_FRONTEND=noninteractive \
    CONDA_DIR="/opt/conda" \
    PYTHONPATH="/opt/conda/lib/python3.10/site-packages"

# Install system dependencies in fewer layers
RUN apt-get update && apt-get install -y \
    apt-utils wget unzip g++ gcc make valgrind heaptrack nano \
    libgsl-dev libncurses5-dev libbz2-dev liblzma-dev git-all \
    dos2unix default-jre cmake zlib1g-dev build-essential \
    libgsl0-dev bedtools mummer perl libncursesw5-dev \
    libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev \
    python3-tk ncbi-blast+ libglpk-dev r-base-core exonerate \
    barrnap bc parallel curl libcurl4-openssl-dev libsbml5-dev \
    r-base libisal-dev less locales && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set locale
RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8

# Install Miniforge and configure conda
RUN wget -q --retry-connrefused --waitretry=1 --read-timeout=20 --timeout=15 -t 3 \
    https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh \
    -O /tmp/miniforge.sh && \
    bash /tmp/miniforge.sh -b -p ${CONDA_DIR} && \
    rm /tmp/miniforge.sh

ENV PATH=${CONDA_DIR}/bin:$PATH

# Configure conda channels and update
RUN conda config --add channels defaults && \
    conda config --add channels conda-forge && \
    conda config --add channels bioconda && \
    conda config --set channel_priority flexible && \
    mamba update -y conda mamba

# Install Python and core packages
RUN mamba install -y python=3.10 && \
    mamba install -y -c conda-forge \
        numpy cython psutil pandas matplotlib scipy seaborn \
        'scikit-learn>=1.2,<1.4' r-base glpk r-sybil r-httr && \
    mamba install -y -c bioconda \
        biopython pysam r-optparse

# Install bioinformatics tools
RUN mamba install -y -c bioconda \
        metabat2 maxbin2 concoct checkm-genome \
        samtools bowtie2 bwa fastp vsearch salmon \
        spades prodigal hmmer mash fastani bbmap \
        cd-hit pplacer gtdbtk=2.4.1

# Create tools directory and set working directory
WORKDIR /quackers_tools

# Install Python 2.7 from source for Ubuntu 24.04 (required for MetaWRAP)
RUN apt-get update && \
    apt-get install -y wget build-essential zlib1g-dev libncurses5-dev \
                       libgdbm-dev libnss3-dev libssl-dev libreadline-dev \
                       libffi-dev libsqlite3-dev libbz2-dev && \
    wget -q https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tgz && \
    tar -xzf Python-2.7.18.tgz && \
    cd Python-2.7.18 && \
    ./configure --prefix=/usr/local --disable-test-modules && \
    make -j$(nproc) && \
    make altinstall && \
    cd .. && \
    rm -rf Python-2.7.18* && \
    ln -sf /usr/local/bin/python2.7 /usr/local/bin/python2 && \
    curl -s https://bootstrap.pypa.io/pip/2.7/get-pip.py | PYTHONPATH="" /usr/local/bin/python2.7 && \
    PYTHONPATH="" /usr/local/bin/pip2.7 install --no-cache-dir numpy==1.16.6 biopython==1.76 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install additional tools from source
RUN wget -q https://github.com/voutcn/megahit/releases/download/v1.2.9/MEGAHIT-1.2.9-Linux-x86_64-static.tar.gz && \
    tar -xzf MEGAHIT-1.2.9-Linux-x86_64-static.tar.gz && \
    mv MEGAHIT-1.2.9-Linux-x86_64-static megahit && \
    rm *.tar.gz

# Install AdapterRemoval
RUN wget -q https://github.com/MikkelSchubert/adapterremoval/archive/v2.3.4.tar.gz && \
    tar -xzf v2.3.4.tar.gz && \
    cd adapterremoval-2.3.4 && \
    make && \
    cp build/AdapterRemoval ${CONDA_DIR}/bin/ && \
    cd .. && \
    rm -rf adapterremoval-2.3.4 v2.3.4.tar.gz

# Install BWA-MEM2
RUN wget -q https://github.com/bwa-mem2/bwa-mem2/releases/download/v2.2.1/bwa-mem2-2.2.1_x64-linux.tar.bz2 && \
    tar -xf bwa-mem2-2.2.1_x64-linux.tar.bz2 && \
    cp bwa-mem2-2.2.1_x64-linux/bwa-mem2* ${CONDA_DIR}/bin/ && \
    rm -rf bwa-mem2-2.2.1_x64-linux*

# Install skani and FastTree
RUN wget -q https://github.com/bluenote-1577/skani/releases/download/latest/skani && \
    chmod +x skani && \
    mv skani ${CONDA_DIR}/bin/ && \
    wget -q http://www.microbesonline.org/fasttree/FastTree && \
    chmod +x FastTree && \
    mv FastTree ${CONDA_DIR}/bin/ && \
    wget -q http://www.microbesonline.org/fasttree/FastTreeMP && \
    chmod +x FastTreeMP && \
    mv FastTreeMP ${CONDA_DIR}/bin/

# Install MetaWRAP and related modules
RUN wget -q https://compsysbio.org/metawrap_mod/metawrap_modules.tar.gz && \
    tar -xzf metawrap_modules.tar.gz && \
    wget -q https://compsysbio.org/metawrap_mod/metawrap_scripts.tar.gz && \
    tar -xzf metawrap_scripts.tar.gz && \
    git clone --depth 1 https://github.com/bxlab/metaWRAP.git metaWRAP-1.3 && \
    rm *.tar.gz

# Install BBMap
RUN wget -q https://sourceforge.net/projects/bbmap/files/BBMap_39.08.tar.gz && \
    tar -xzf BBMap_39.08.tar.gz && \
    rm *.tar.gz

# Install gapseq
RUN git clone --depth 1 https://github.com/jotech/gapseq.git

# Install additional Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        python-libsbml networkx plotly dash jupyterlab

# Create database directories
RUN mkdir -p gtdbtk_data checkm_data pfam_db ncbi_hmms cog_db

# Create simple database download script
RUN { \
    echo '#!/bin/bash'; \
    echo 'set -euo pipefail'; \
    echo ''; \
    echo '# Simple database download script'; \
    echo '# Usage: ./download_databases.sh [BASE_PATH]'; \
    echo ''; \
    echo 'BASE_PATH="${1:-/quackers_tools}"'; \
    echo ''; \
    echo '# Define subdirectory paths'; \
    echo 'GTDB_PATH="$BASE_PATH/gtdbtk_data"'; \
    echo 'CHECKM_PATH="$BASE_PATH/checkm_data"'; \
    echo 'PFAM_PATH="$BASE_PATH/pfam_db"'; \
    echo 'NCBI_PATH="$BASE_PATH/ncbi_hmms"'; \
    echo 'COG_PATH="$BASE_PATH/cog_db"'; \
    echo ''; \
    echo 'echo "=== Database Download ==="'; \
    echo 'echo "Base directory: $BASE_PATH"'; \
    echo 'echo "Downloading essential databases..."'; \
    echo 'echo ""'; \
    echo ''; \
    echo '# Create directories'; \
    echo 'mkdir -p "$GTDB_PATH" "$CHECKM_PATH" "$PFAM_PATH" "$NCBI_PATH" "$COG_PATH"'; \
    echo ''; \
    echo '# Download CheckM (275MB)'; \
    echo 'echo "[1/4] Downloading CheckM database..."'; \
    echo 'cd "$CHECKM_PATH"'; \
    echo 'wget -q --show-progress "https://data.ace.uq.edu.au/public/CheckM_databases/checkm_data_2015_01_16.tar.gz"'; \
    echo 'tar -xzf checkm_data_2015_01_16.tar.gz && rm checkm_data_2015_01_16.tar.gz'; \
    echo 'echo "✓ CheckM complete"'; \
    echo ''; \
    echo '# Download Pfam (500MB)'; \
    echo 'echo "[2/4] Downloading Pfam database..."'; \
    echo 'cd "$PFAM_PATH"'; \
    echo 'wget -q --show-progress "https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz"'; \
    echo 'gunzip Pfam-A.hmm.gz'; \
    echo 'echo "✓ Pfam complete"'; \
    echo ''; \
    echo '# Download NCBI HMMs (1GB)'; \
    echo 'echo "[3/4] Downloading NCBI HMMs..."'; \
    echo 'cd "$NCBI_PATH"'; \
    echo 'wget -q --show-progress "https://ftp.ncbi.nlm.nih.gov/hmm/current/hmm_PGAP.HMM.tgz"'; \
    echo 'tar -xzf hmm_PGAP.HMM.tgz && rm hmm_PGAP.HMM.tgz'; \
    echo 'echo "✓ NCBI HMMs complete"'; \
    echo ''; \
    echo '# Download COG (100MB)'; \
    echo 'echo "[4/4] Downloading COG database..."'; \
    echo 'cd "$COG_PATH"'; \
    echo 'wget -q --show-progress "https://ftp.ncbi.nlm.nih.gov/pub/COG/COG2024/data/cog-24.cog.csv"'; \
    echo 'wget -q --show-progress "https://ftp.ncbi.nlm.nih.gov/pub/COG/COG2024/data/cog-24.def.tab"'; \
    echo 'echo "✓ COG complete"'; \
    echo ''; \
    echo 'echo ""'; \
    echo 'echo "=== Essential Databases Downloaded ==="'; \
    echo 'echo "Location: $BASE_PATH"'; \
    echo 'echo ""'; \
    echo 'echo "To download GTDB-Tk database (~80GB):"'; \
    echo 'echo "cd $GTDB_PATH"'; \
    echo 'echo "wget https://data.ace.uq.edu.au/public/gtdb/data/releases/release220/220.0/auxillary_files/gtdbtk_package/full_package/gtdbtk_r220_data.tar.gz"'; \
    echo 'echo "tar -xzf gtdbtk_r220_data.tar.gz && rm gtdbtk_r220_data.tar.gz"'; \
    echo 'echo ""'; \
    echo 'echo "Environment variables:"'; \
    echo 'echo "export GTDBTK_DATA_PATH=\"$GTDB_PATH\""'; \
    echo 'echo "export CHECKM_DATA_PATH=\"$CHECKM_PATH\""'; \
    echo 'echo "export PFAM_DB_PATH=\"$PFAM_PATH\""'; \
    echo 'echo "export NCBI_HMMS_PATH=\"$NCBI_PATH\""'; \
    echo 'echo "export COG_DB_PATH=\"$COG_PATH\""'; \
    } > download_databases.sh && chmod +x download_databases.sh

# Set up pipeline directory and download scripts
WORKDIR /quackers_pipe

# Download pipeline files in parallel
RUN { \
    wget -q https://raw.githubusercontent.com/ParkinsonLab/quackers/test/quackers_pipe.py & \
    wget -q https://raw.githubusercontent.com/ParkinsonLab/quackers/test/quackers_commands.py & \
    wget -q https://raw.githubusercontent.com/ParkinsonLab/quackers/test/MetaPro_utilities_v2.py & \
    wget -q https://raw.githubusercontent.com/ParkinsonLab/quackers/test/quackers_stages.py & \
    wget -q https://raw.githubusercontent.com/ParkinsonLab/quackers/test/quackers_paths.py & \
    wget -q https://raw.githubusercontent.com/ParkinsonLab/quackers/test/Config.ini & \
    wait; \
    }

# Download additional scripts
RUN mkdir -p scripts modded_scripts && \
    cd scripts && \
    { \
    wget -q https://raw.githubusercontent.com/ParkinsonLab/quackers/test/scripts/contig_reconcile.py & \
    wget -q https://raw.githubusercontent.com/ParkinsonLab/quackers/test/scripts/sam_sift.py & \
    wget -q https://raw.githubusercontent.com/ParkinsonLab/quackers/test/scripts/clean_reads_reconcile.py & \
    wait; \
    } && \
    cd ../modded_scripts && \
    { \
    wget -q https://raw.githubusercontent.com/ParkinsonLab/quackers/test/modded_scripts/concoct_coverage_table.py & \
    wget -q https://raw.githubusercontent.com/ParkinsonLab/quackers/test/modded_scripts/extract_fasta_bins.py & \
    wget -q https://raw.githubusercontent.com/ParkinsonLab/quackers/test/modded_scripts/merge_cutup_clustering.py & \
    wget -q https://raw.githubusercontent.com/ParkinsonLab/quackers/test/modded_scripts/print_comment.py & \
    wait; \
    }

# Set environment variables
ENV CHECKM_DATA_PATH=/quackers_tools/checkm_data \
    GTDBTK_DATA_PATH=/quackers_tools/gtdbtk_data \
    PATH="${PATH}:/quackers_tools/metaWRAP-1.3/bin:/quackers_tools/megahit/bin:/quackers_tools/gapseq/gapseq:/quackers_tools/bbmap"

# Test key installations (with proper syntax for each tool)
RUN echo "Testing tool installations..." && \
    concoct --help > /dev/null 2>&1 && \
    (checkm > /dev/null 2>&1 || true) && \
    gtdbtk --help > /dev/null 2>&1 && \
    metabat2 --help > /dev/null 2>&1 && \
    samtools --version > /dev/null && \
    python --version && \
    echo "All tools installed successfully!" && \
    echo "" && \
    echo "=== IMPORTANT: Database Setup Required ===" && \
    echo "Run './download_databases.sh' after container starts" && \
    echo "This requires ~2GB space for essential databases" && \
    echo "GTDB-Tk database (~80GB) can be downloaded separately" && \
    echo "Or mount external database volumes at:" && \
    echo "  $GTDBTK_DATA_PATH" && \
    echo "  $CHECKM_DATA_PATH"

# Create health check script
RUN { \
    echo '#!/bin/bash'; \
    echo 'echo "=== Tool Health Check ==="'; \
    echo 'echo -n "concoct: "'; \
    echo 'if concoct --help >/dev/null 2>&1; then echo "✓ available"; else echo "✗ missing"; fi'; \
    echo 'echo -n "checkm: "'; \
    echo 'if checkm >/dev/null 2>&1 || [[ $? -eq 2 ]]; then echo "✓ available"; else echo "✗ missing"; fi'; \
    echo 'echo -n "gtdbtk: "'; \
    echo 'if gtdbtk --help >/dev/null 2>&1; then echo "✓ available"; else echo "✗ missing"; fi'; \
    echo 'echo -n "metabat2: "'; \
    echo 'if metabat2 --help >/dev/null 2>&1; then echo "✓ available"; else echo "✗ missing"; fi'; \
    echo 'echo -n "samtools: "'; \
    echo 'if samtools --version >/dev/null 2>&1; then echo "✓ available"; else echo "✗ missing"; fi'; \
    echo 'echo -n "python: "'; \
    echo 'if python --version >/dev/null 2>&1; then echo "✓ available"; else echo "✗ missing"; fi'; \
    echo 'echo -n "python2: "'; \
    echo 'if python2 --version >/dev/null 2>&1; then echo "✓ available"; else echo "✗ missing"; fi'; \
    echo 'echo "=== Database Status ==="'; \
    echo 'for db in "$CHECKM_DATA_PATH" "$GTDBTK_DATA_PATH"; do'; \
    echo '    if [[ -d "$db" && -n "$(ls -A "$db" 2>/dev/null)" ]]; then'; \
    echo '        echo "✓ $(basename "$db"): ready"'; \
    echo '    else'; \
    echo '        echo "✗ $(basename "$db"): not found or empty"'; \
    echo '    fi'; \
    echo 'done'; \
    } > /usr/local/bin/health_check.sh && chmod +x /usr/local/bin/health_check.sh

# Final cleanup
RUN mamba clean -a -y && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    find /quackers_tools -type f -name "*.tar.gz" -delete 2>/dev/null || true && \
    find /quackers_tools -type f -name "*.tgz" -delete 2>/dev/null || true

# Set permissions
RUN chmod -R 755 /quackers_tools && \
    chmod -R 755 /quackers_pipe

# Add labels for better container management
LABEL maintainer="Quackers Pipeline" \
      version="3.1.0" \
      description="Optimized bioinformatics container for metagenomics analysis" \
      tools="MetaWRAP,GTDB-Tk,CheckM,MetaBat2,CONCOCT,MaxBin2" \
      python.versions="3.10,2.7"

WORKDIR /quackers_pipe

# Show information on startup
CMD echo "=== Quackers Pipeline Container ===" && \
    echo "Run 'health_check.sh' to verify installation" && \
    echo "Run './download_databases.sh' to download essential databases (~2GB)" && \
    echo "For GTDB-Tk: see script output for manual download instructions" && \
    echo "Container ready!" && \
    bash