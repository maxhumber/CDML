#### Deploy: Dokku



Update environment

```
pip install tensorflow
```

3. Freeze the dependencies:

```
pip freeze > requirements.txt
```

4. Retrain the model inside of the virtual environment:

```
python model.py
```

5. Make sure the app still works locally:

```
python app.py
```

6. Push everything up to GitHub:

```
git add .
git commit -m '🚀'
git push
```



#### Bonus: Custom Domain Instructions



**On Namecheap**

1. Add the following DNS records:

| Type                | Host | Value                                        | TTL       |
| ------------------- | ---- | -------------------------------------------- | --------- |
| A Record            | @    | 165.XXX.43.118                               | Automatic |
| URL Redirect Record | www  | http://fantasyfootball.ninja (Permanent 301) |           |
| A Record            | *    | 165.XXX.43.118                               | Automatic |

**On Server**

2. ssh into `root@165.XXX.43.118`

3. Install the Let’s Encrypt plugin for Dokku:

```
sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
```

4. Set the `DOKKU_LETSENCRYPT_EMAIL` environment variable to the email for Let’s Encrypt:

```
dokku config:set ffninja DOKKU_LETSENCRYPT_EMAIL=first.last@email.com
```

5. Add the application and domain (http://`scrape.world` is the actual domain!):

```
dokku domains:add ffninja fantasyfootball.ninja
```

6. Create the SSL certificate. NGINX will automatically start serving the application over HTTPS on port 443:

```
dokku letsencrypt ffninja
```

7. Run this as a cron job so the certificate will renew automatically:.

```
dokku letsencrypt:cron-job --add
```
