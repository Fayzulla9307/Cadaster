# Statement for enabling the development environment
DEBUG = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database 
#SQLALCHEMY_DATABASE_URI = "mysql://balans:RathowtOjpydedNo@localhost/balans"

SQLALCHEMY_DATABASE_URI = "mysql://root:F.yusup0v@localhost/balans"

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 10

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "kamnakosyonBaljIpMishlanUnEvosbo"

# Secret key for signing cookies
SECRET_KEY = "ew0BlawpAcyajNirshesUvonViUjEbs1"

# Token key
TOKEN_KEY = "OogyejIvumNasAdUbBishkOudGajnicPiWrymagAbthucradocviOrmosOvDerow"

# Server nonce
SERVER_NONCE = "RabroyllIjhywofuckcorwojnamvowAg"

# Validity of the token in days
JWT_VALIDITY_IN_DAYS = 30

# Report directory
REPORT_OUTPUT_FOLDER = "output"
