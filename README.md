# Cloud Data Exporter

Upload data from the public cloud you are running on to your Zenodo space.  
This tool **does not** publish content but just uploads it.

## Follow these steps to export data:

## 1. Create a Zenodo account
Go to [Zenodo](https://zenodo.org/signup/) to open an account to which your data will be exported.  
For more testing purposes you can also use [sandbox.zenodo](https://sandbox.zenodo.org/signup/).  
**[Note that an account on one of the options doesn't give access to the other. Same thing applies to access tokens]**

## 2. Create an access token
Once logged in to Zenodo, go to Account / Applications to create an access token that will be used to upload files.

## 3. Download and prepare
On the VM from which you want to export the data, clone this repo and cd into it:
```bash
git clone https://github.com/ignpelloz/cloud-exporter.git
cd cloud-exporter
```
**Modify the file configs.yaml according to your upload.**

| Property	| Explanation / Values |
| ------------- | ---------------------- |
|`access_token` | The access token previously created |
|`path_to_data` | Path to the file or dir you desire to export, including the name of such file or dir |
|`title` | Title you want to give your upload |
|`sandbox` | Boolean. True: use sandbox.zenodo / False: use zenodo. Default is False |

## 4. Run the tool
```bash
#python2 (default)
pip install requests pyyaml
./cloud-exporter.py
```
```bash
#python3
pip install requests pyyaml
python3 cloud-exporter.py
```
Log messages will be printed to the console informing the steps being carried out. At the end of it your content will be available at Zenodo.

*****

**This tool has been tested on:**  
Python: 2 and 3  
OS: Ubuntu, Centos, OpenBSD, Debian, Red Hat, Windows

*****

**License**  

Copyright (c) CERN

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
