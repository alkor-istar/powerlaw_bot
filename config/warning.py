# warnings_config.py
import warnings
from swagger_spec_validator.common import SwaggerValidationWarning

warnings.filterwarnings(
    "ignore",
    category=SwaggerValidationWarning,
)

warnings.filterwarnings(
    "ignore",
    message=r".*guid format is not registered with bravado-core.*",
    module=r"bravado_core\.spec",
)
