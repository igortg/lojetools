from distutils.core import setup
import py2exe

  
bin_excludes = [
    "msvcr90.dll",
    "msvcp90.dll",
    "msvcr90d.dll",
    "msvcp90d.dll",
    "w9xpopen.exe"
    "AVICAP32.dll", # DLLs included when building on Vista
    "AVIFIL32.dll",
    "dhcpcsvc6.dll",
    "iphlpapi.dll",
    "DNSAPI.dll",
    "MSACM32.dll",
    "MSVFW32.dll",
    "NSI.dll",
    "WINNSI.dll",
]


setup(
    name='Theves Etiquetas',
    windows = [{
        'dest_base'      : 'theves_etiquetas',
        'script'         : '../src/lojeproductsheet_ui.pyw',
    }],
    options = {
        "py2exe": {
            "bundle_files" : 3, 
            'dll_excludes' : bin_excludes,
			'compressed'   : True,  # Compressed executable
        }
    },
	# Uncomment the line below if you are using matplotlib
	#data_files=matplotlib.get_py2exe_datafiles(),
    # zipfile=None
)
