from itertools import chain

from setuptools import setup

# at least 1.3 to be able to use XMLDataset and pandas integration with fsspec
PANDAS = "pandas>=1.3, <3.0"
SPARK = "pyspark>=2.2, <4.0"
HDFS = "hdfs>=2.5.8, <3.0"
S3FS = "s3fs>=2021.4, <2024.1"  # Upper bound set arbitrarily, to be reassessed in early 2024
POLARS = "polars>=0.18.0"
DELTA = "delta-spark~=1.2.1"


def _collect_requirements(requires):
    return sorted(set(chain.from_iterable(requires.values())))


api_require = {"api.APIDataset": ["requests~=2.20"]}
biosequence_require = {"biosequence.BioSequenceDataset": ["biopython~=1.73"]}
dask_require = {
    "dask.ParquetDataset": ["dask[complete]>=2021.10", "triad>=0.6.7, <1.0"]
}
databricks_require = {"databricks.ManagedTableDataset": [SPARK, PANDAS, DELTA]}
geopandas_require = {
    "geopandas.GeoJSONDataset": ["geopandas>=0.6.0, <1.0", "pyproj~=3.0"]
}
holoviews_require = {"holoviews.HoloviewsWriter": ["holoviews~=1.13.0"]}
huggingface_require = {
    "huggingface.HFDataset": ["datasets", "huggingface_hub"],
    "huggingface.HFTransformerPipelineDataset": ["transformers"],
}
matplotlib_require = {"matplotlib.MatplotlibWriter": ["matplotlib>=3.0.3, <4.0"]}
matlab_require = {"matlab.MatlabDataset": ["scipy"]}
networkx_require = {"networkx.NetworkXDataset": ["networkx~=2.4"]}
pandas_require = {
    "pandas.CSVDataset": [PANDAS],
    "pandas.ExcelDataset": [PANDAS, "openpyxl>=3.0.6, <4.0"],
    "pandas.DeltaTableDataset": [PANDAS, "deltalake>=0.10.0"],
    "pandas.FeatherDataset": [PANDAS],
    "pandas.GBQTableDataset": [
        PANDAS,
        "pandas-gbq>=0.12.0, <0.18.0; python_version < '3.11'",
        "pandas-gbq>=0.18.0; python_version >= '3.11'",
    ],
    "pandas.GBQQueryDataset": [
        PANDAS,
        "pandas-gbq>=0.12.0, <0.18.0; python_version < '3.11'",
        "pandas-gbq>=0.18.0; python_version >= '3.11'",
    ],
    "pandas.HDFDataset": [
        PANDAS,
        "tables~=3.6",
    ],
    "pandas.JSONDataset": [PANDAS],
    "pandas.ParquetDataset": [PANDAS, "pyarrow>=6.0"],
    "pandas.SQLTableDataset": [PANDAS, "SQLAlchemy>=1.4, <3.0"],
    "pandas.SQLQueryDataset": [PANDAS, "SQLAlchemy>=1.4, <3.0", "pyodbc~=4.0"],
    "pandas.XMLDataset": [PANDAS, "lxml~=4.6"],
    "pandas.GenericDataset": [PANDAS],
}
pickle_require = {"pickle.PickleDataset": ["compress-pickle[lz4]~=2.1.0"]}
pillow_require = {"pillow.ImageDataset": ["Pillow~=9.0"]}
plotly_require = {
    "plotly.PlotlyDataset": [PANDAS, "plotly>=4.8.0, <6.0"],
    "plotly.JSONDataset": ["plotly>=4.8.0, <6.0"],
}
polars_require = {
    "polars.CSVDataset": [POLARS],
    "polars.GenericDataset": [
        POLARS,
        "pyarrow>=4.0",
        "xlsx2csv>=0.8.0",
        "deltalake >= 0.6.2",
    ],
    "polars.EagerPolarsDataset": [
        POLARS,
        "pyarrow>=4.0",
        "xlsx2csv>=0.8.0",
        "deltalake >= 0.6.2",
    ],
    "polars.LazyPolarsDataset": [
        # Note: there is no Lazy read Excel option, so we exclude xlsx2csv here.
        POLARS,
        "pyarrow>=4.0",
        "deltalake >= 0.6.2",
    ],
}
redis_require = {"redis.PickleDataset": ["redis~=4.1"]}
snowflake_require = {
    "snowflake.SnowparkTableDataset": [
        "snowflake-snowpark-python~=1.0",
        "pyarrow~=8.0",
    ]
}
spark_require = {
    "spark.SparkDataset": [SPARK, HDFS, S3FS],
    "spark.SparkHiveDataset": [SPARK, HDFS, S3FS],
    "spark.SparkJDBCDataset": [SPARK, HDFS, S3FS],
    "spark.DeltaTableDataset": [SPARK, HDFS, S3FS, "delta-spark>=1.0, <3.0"],
}
svmlight_require = {"svmlight.SVMLightDataset": ["scikit-learn>=1.0.2", "scipy~=1.7.3"]}
tensorflow_require = {
    "tensorflow.TensorFlowModelDataset": [
        # currently only TensorFlow V2 supported for saving and loading.
        # V1 requires HDF5 and serialises differently
        "tensorflow~=2.0; platform_system != 'Darwin' or platform_machine != 'arm64'",
        # https://developer.apple.com/metal/tensorflow-plugin/
        "tensorflow-macos~=2.0; platform_system == 'Darwin' and platform_machine == 'arm64'",
    ]
}
video_require = {"video.VideoDataset": ["opencv-python~=4.5.5.64"]}
yaml_require = {"yaml.YAMLDataset": [PANDAS, "PyYAML>=4.2, <7.0"]}

extras_require = {
    "api": _collect_requirements(api_require),
    "biosequence": _collect_requirements(biosequence_require),
    "dask": _collect_requirements(dask_require),
    "databricks": _collect_requirements(databricks_require),
    "geopandas": _collect_requirements(geopandas_require),
    "holoviews": _collect_requirements(holoviews_require),
    "huggingface": _collect_requirements(huggingface_require),
    "matlab": _collect_requirements(matlab_require),
    "matplotlib": _collect_requirements(matplotlib_require),
    "networkx": _collect_requirements(networkx_require),
    "pandas": _collect_requirements(pandas_require),
    "pickle": _collect_requirements(pickle_require),
    "pillow": _collect_requirements(pillow_require),
    "plotly": _collect_requirements(plotly_require),
    "polars": _collect_requirements(polars_require),
    "redis": _collect_requirements(redis_require),
    "snowflake": _collect_requirements(snowflake_require),
    "spark": _collect_requirements(spark_require),
    "svmlight": _collect_requirements(svmlight_require),
    "tensorflow": _collect_requirements(tensorflow_require),
    "video": _collect_requirements(video_require),
    "yaml": _collect_requirements(yaml_require),
    **api_require,
    **biosequence_require,
    **dask_require,
    **databricks_require,
    **geopandas_require,
    **holoviews_require,
    **matplotlib_require,
    **networkx_require,
    **pandas_require,
    **pickle_require,
    **pillow_require,
    **plotly_require,
    **polars_require,
    **snowflake_require,
    **spark_require,
    **svmlight_require,
    **tensorflow_require,
    **video_require,
    **yaml_require,
}

extras_require["all"] = _collect_requirements(extras_require)
extras_require["docs"] = [
    # docutils>=0.17 changed the HTML
    # see https://github.com/readthedocs/sphinx_rtd_theme/issues/1115
    "docutils==0.16",
    "sphinx~=5.3.0",
    "sphinx_rtd_theme==1.2.0",
    # Regression on sphinx-autodoc-typehints 1.21
    # that creates some problematic docstrings
    "sphinx-autodoc-typehints==1.20.2",
    "sphinx_copybutton==0.3.1",
    "sphinx-notfound-page",
    "ipykernel>=5.3, <7.0",
    "sphinxcontrib-mermaid~=0.7.1",
    "myst-parser~=1.0.0",
    "Jinja2<3.1.0",
]
extras_require["test"] = [
    "adlfs~=2023.1",
    "bandit>=1.6.2, <2.0",
    "behave==1.2.6",
    "biopython~=1.73",
    "blacken-docs==1.9.2",
    "black~=22.0",
    "cloudpickle<=2.0.0",
    "compress-pickle[lz4]~=2.1.0",
    "coverage[toml]",
    "dask[complete]>=2021.10",
    "delta-spark>=1.0, <3.0",
    "deltalake>=0.10.0",
    "dill~=0.3.1",
    "filelock>=3.4.0, <4.0",
    "gcsfs>=2023.1, <2023.3",
    "geopandas>=0.6.0, <1.0",
    "hdfs>=2.5.8, <3.0",
    "holoviews>=1.13.0",
    "import-linter[toml]==1.2.6",
    "ipython>=7.31.1, <8.0",
    "Jinja2<3.1.0",
    "joblib>=0.14",
    "jupyterlab~=3.0",
    "jupyter~=1.0",
    "lxml~=4.6",
    "matplotlib>=3.0.3, <3.4; python_version < '3.10'",  # 3.4.0 breaks holoviews
    "matplotlib>=3.5, <3.6; python_version >= '3.10'",
    "memory_profiler>=0.50.0, <1.0",
    "moto==1.3.7; python_version < '3.10'",
    "moto==4.1.12; python_version >= '3.10'",
    "networkx~=2.4",
    "opencv-python~=4.5.5.64",
    "openpyxl>=3.0.3, <4.0",
    "pandas-gbq>=0.12.0, <0.18.0; python_version < '3.11'",
    "pandas-gbq>=0.18.0; python_version >= '3.11'",
    "pandas~=1.3  # 1.3 for read_xml/to_xml",
    "Pillow~=9.0",
    "plotly>=4.8.0, <6.0",
    "polars[xlsx2csv, deltalake]~=0.18.0",
    "pre-commit>=2.9.2",
    "pyarrow>=1.0; python_version < '3.11'",
    "pyarrow>=7.0; python_version >= '3.11'",  # Adding to avoid numpy build errors
    "pyodbc~=4.0.35",
    "pyproj~=3.0",
    "pyspark>=2.2, <3.4; python_version < '3.11'",
    "pyspark>=3.4; python_version >= '3.11'",
    "pytest-cov~=3.0",
    "pytest-mock>=1.7.1, <2.0",
    "pytest-xdist[psutil]~=2.2.1",
    "pytest~=7.2",
    "redis~=4.1",
    "requests-mock~=1.6",
    "requests~=2.20",
    "ruff~=0.0.290",
    "s3fs>=2021.04, <2024.1",
    "snowflake-snowpark-python~=1.0; python_version == '3.9'",
    "scikit-learn>=1.0.2,<2",
    "scipy>=1.7.3",
    "packaging",
    "SQLAlchemy~=1.2",
    "tables~=3.8.0; platform_system == 'Windows'",  # Import issues with python 3.8 with pytables pinning to 3.8.0 fixes this https://github.com/PyTables/PyTables/issues/933#issuecomment-1555917593
    "tables~=3.6; platform_system != 'Windows'",
    "tensorflow-macos~=2.0; platform_system == 'Darwin' and platform_machine == 'arm64'",
    "tensorflow~=2.0; platform_system != 'Darwin' or platform_machine != 'arm64'",
    "triad>=0.6.7, <1.0",
    "trufflehog~=2.1",
    "xlsxwriter~=1.0",
    # huggingface
    "datasets",
    "huggingface_hub",
    "transformers",
]

setup(
    extras_require=extras_require,
)
