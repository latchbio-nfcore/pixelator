process PIXELATOR_DEMUX {
    tag "$meta.id"
    label 'process_medium'

    // TODO: Update once pixelator is public in bioconda
    conda "local::pixelator=0.13.0"
    container "ghcr.io/pixelgentechnologies/pixelator:0.13.0"

    input:
    tuple val(meta), path(reads), path(panel_file), val(panel)

    output:
    tuple val(meta), path("demux/*processed*.{fq,fastq}.gz"), emit: processed
    tuple val(meta), path("demux/*failed.{fq,fastq}.gz")    , emit: failed
    tuple val(meta), path("demux/*.report.json")            , emit: report_json
    tuple val(meta), path("demux/*.meta.json")              , emit: metadata
    tuple val(meta), path("*pixelator-demux.log")           , emit: log

    path "versions.yml"                                     , emit: versions

    when:
    task.ext.when == null || task.ext.when

    script:
    // --design is passed in meta and added to args through modules.conf

    prefix = task.ext.prefix ?: "${meta.id}"
    def args = task.ext.args ?: ''
    def panelOpt = (
        panel      ? "--panel $panel"      :
        panel_file ? "--panel $panel_file" :
        ""
    )

    """
    pixelator \\
        --cores $task.cpus \\
        --log-file ${prefix}.pixelator-demux.log \\
        --verbose \\
        single-cell \\
        demux \\
        --output . \\
        $panelOpt \\
        $args \\
        ${reads}

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        pixelator: \$(echo \$(pixelator --version 2>/dev/null) | sed 's/pixelator, version //g' )
    END_VERSIONS
    """
}
