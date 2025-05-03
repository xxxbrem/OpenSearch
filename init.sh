apt update 
apt upgrade -y
apt install unzip
pip install -r requirements.txt
cd Spider2-sqlite
mkdir test_database
cd test_database
gdown 'https://drive.google.com/uc?id=1coEVsCZq-Xvj9p2TnhBFoFTsY-UoYGmG'
unzip local_sqlite.zip
cd ..
python mk_db.py