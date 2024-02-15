docker run -it\
 -v "$(pwd):/home/app"\
 -e APP_URI="your_uri"\
 -e AWS_ACCESS_KEY_ID="your_acces_key"\
 -e AWS_SECRET_ACCESS_KEY="your_secret_access_key"\
 train