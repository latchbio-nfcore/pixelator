
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'input_basedir': NextflowParameter(
        type=typing.Optional[LatchDir],
        default=None,
        section_title=None,
        description='Path to a local or remote directory that is the "current working directory" for relative paths defined in the input samplesheet',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'trim_front': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title='QC/Filtering/Trimming options',
        description='Trim N bases from the front of the reads',
    ),
    'trim_tail': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title=None,
        description='Trim N bases from the tail of the reads',
    ),
    'max_length': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='The maximum length of a read',
    ),
    'min_length': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='The minimum length (bases) of a read',
    ),
    'max_n_bases': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title=None,
        description='The maximum number of Ns allowed in a read',
    ),
    'avg_qual': NextflowParameter(
        type=typing.Optional[int],
        default=20,
        section_title=None,
        description='Minimum avg. quality a read must have (0 will disable the filter)',
    ),
    'dedup': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Remove duplicated reads (exact same sequence)',
    ),
    'remove_polyg': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Remove PolyG sequences (length of 10 or more)',
    ),
    'adapterqc_mismatches': NextflowParameter(
        type=typing.Optional[float],
        default=0.1,
        section_title='Adapter QC Options',
        description='The number of mismatches allowed (in percentage) [default: 0.1; 0.0<=x<=0.9]',
    ),
    'demux_mismatches': NextflowParameter(
        type=typing.Optional[float],
        default=0.1,
        section_title='Demux options',
        description='The number of mismatches allowed (as a fraction)',
    ),
    'demux_min_length': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='The minimum length of the barcode that must overlap when matching',
    ),
    'markers_ignore': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Collapse options',
        description='A list of comma separated antibodies to discard',
    ),
    'algorithm': NextflowParameter(
        type=typing.Optional[str],
        default='adjacency',
        section_title=None,
        description='The algorithm to use for collapsing (adjacency will perform error correction using the number of mismatches given)',
    ),
    'collapse_mismatches': NextflowParameter(
        type=typing.Optional[int],
        default=2,
        section_title=None,
        description='The number of mismatches allowed when collapsing (adjacency)',
    ),
    'collapse_min_count': NextflowParameter(
        type=typing.Optional[int],
        default=2,
        section_title=None,
        description='Discard molecules with with a count (reads) lower than this value',
    ),
    'collapse_use_counts': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Use counts when collapsing (the difference in counts between two molecules must be more than double in order to be collapsed)',
    ),
    'multiplet_recovery': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title='Options for pixelator graph command.',
        description='Activate the multiplet recovery using leiden community detection',
    ),
    'min_size': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title='Options for pixelator annotate command.',
        description='The minimum size (pixels) a component/cell can have (disabled by default)',
    ),
    'max_size': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='The maximum size (pixels) a component/cell can have (disabled by default)',
    ),
    'dynamic_filter': NextflowParameter(
        type=typing.Optional[str],
        default='min',
        section_title=None,
        description=' Enable the estimation of dynamic size filters using a log-rank approach both: estimate both min and max size, min: estimate min size (--min-size), max: estimate max size (--max-size)',
    ),
    'aggregate_calling': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Enable aggregate calling, information on potential aggregates will be added to the output data',
    ),
    'skip_analysis': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Options for pixelator analysis command.',
        description='Skip analysis step',
    ),
    'compute_polarization': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Compute polarization scores matrix (clusters by markers)',
    ),
    'compute_colocalization': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description=' Compute colocalization scores (marker by marker) for each component',
    ),
    'use_full_bipartite': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Use the bipartite graph instead of the one-node projection when computing polarization, coabundance and colocalization scores',
    ),
    'polarization_transformation': NextflowParameter(
        type=typing.Optional[str],
        default='log1p',
        section_title=None,
        description='Which transformation to use for the antibody counts when calculating polarity scores.',
    ),
    'polarization_n_permutations': NextflowParameter(
        type=typing.Optional[int],
        default=50,
        section_title=None,
        description='Set the number of permutations use to compute the empirical z- and p-values for the polarity score',
    ),
    'polarization_min_marker_count': NextflowParameter(
        type=typing.Optional[int],
        default=5,
        section_title=None,
        description='The minimum number of counts of a marker to calculate the polarity score in the component',
    ),
    'colocalization_transformation': NextflowParameter(
        type=typing.Optional[str],
        default='log1p',
        section_title=None,
        description='Select the type of transformation to use on the node by antibody counts matrix when computing colocalization',
    ),
    'colocalization_neighbourhood_size': NextflowParameter(
        type=typing.Optional[int],
        default=1,
        section_title=None,
        description='Select the size of the neighborhood to use when computing colocalization metrics on each component',
    ),
    'colocalization_n_permutations': NextflowParameter(
        type=typing.Optional[int],
        default=50,
        section_title=None,
        description='Set the number of permutations use to compute the empirical p-value for the colocalization score',
    ),
    'colocalization_min_region_count': NextflowParameter(
        type=typing.Optional[int],
        default=5,
        section_title=None,
        description='The minimum number of counts in a region for it to be considered valid for computing colocalization',
    ),
    'skip_layout': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Options for pixelator layout command.',
        description='Skip layout step',
    ),
    'no_node_marker_counts': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title=None,
        description='Skip adding marker counts to the layout.',
    ),
    'layout_algorithm': NextflowParameter(
        type=typing.Optional[str],
        default='pmds_3d',
        section_title=None,
        description='Select a layout algorithm to use. This can be specified as a comma separated list to compute multiple layouts. Possible values are: fruchterman_reingold, fruchterman_reingold_3d, kamada_kawai, kamada_kawai_3d, pmds, pmds_3d',
    ),
    'skip_report': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Options for pixelator report command.',
        description='Skip report generation',
    ),
    'pixelator_container': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Global options',
        description='Override the container image reference to use for all steps using the `pixelator` command.',
    ),
}

