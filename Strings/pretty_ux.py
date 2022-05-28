class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

CHECK_MARK =  u'\N{heavy check mark}'
SUCCESS = f"{bcolors.OKGREEN}" + CHECK_MARK + f"{bcolors.ENDC}" # Success 
FAIL = u'\N{cross mark}' # Fail
SPEECH_BALLOON = u'\N{speech balloon}'
CHAINS = u'\N{chains}'