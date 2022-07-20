from .ci import boot_ci
from .ci import cod_ci
from .ci import prd_ci

from .formulas import cod
from .formulas import prd
from .formulas import prb
from .formulas import cod_met
from .formulas import prd_met
from .formulas import prb_met

from .load_data import ratios_sample

from .outliers import quantile_outlier
from .outliers import iqr_outlier
from .outliers import is_outlier

from .sales_chasing import detect_chasing

from .utils import check_inputs