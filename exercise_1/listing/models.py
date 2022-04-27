from timestamps.models import models, Model
        
class Router(Model):
    """Model for Router"""
    class Meta:
        unique_together = (('sap_id', 'hostname', 'loopback', 'mac_address'),)
    # sapId format 1/2/12:1 
    # Reference : https://documentation.nokia.com/cgi-bin/dbaccessfilename.cgi/9304030302_V1_7950%20SR%20OS%20Router%20Configuration%20Guide%2012.0.R4.pdf
    sap_id = models.CharField(max_length=18)
    # hostname restricted to 14 characters as per assignment
    hostname = models.CharField(max_length=14)
    # loopback address range from 127.0.0.1 to 127.255.255.254
    # Reference : https://www.omnisecu.com/tcpip/what-is-loopback-address.php#:~:text=The%20loopback%20network%20in%20IPv4,0.1%20to%20127.255.
    loopback = models.CharField(max_length=15)
    # Mac Address Rules 
    # Reference : https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
    mac_address = models.CharField(max_length=17)
