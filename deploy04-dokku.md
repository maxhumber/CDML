#### Deploy: Dokku



**RESEPCT PORT 5000**?



Change the Procfile

```
echo "web: uvicorn app:app --host=0.0.0.0 --port=80 --workers=2" > Procfile
```

Push everything up to GitHub:

```
git add .
git commit -m '🚀'
git push
```



**On Server**

9. Spin up a $5 Ubuntu 18.04 server ([DigitalOcean](https://m.do.co/c/2909cd1f3f10) works)...

10. ssh into it:

```
ssh root@165.XXX.43.118
```

11. Update everything:

```
sudo apt update
sudo apt -y upgrade
```

12. Get "new" monitoring (DigitalOcean only):

```
curl -sSL https://repos.insights.digitalocean.com/install.sh | sudo bash
```

13. Setup firewall:

````
ufw app list
ufw allow OpenSSH
ufw enable
````

14. Add some rules ([source](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-18-04)):

```
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 22
sudo ufw allow http
sudo ufw allow https
```

Install dokku:

```
wget https://raw.githubusercontent.com/dokku/dokku/v0.21.4/bootstrap.sh
sudo DOKKU_TAG=v0.21.4 bash bootstrap.sh
```

17. Navigate to the machine IP address of the server in a browser and add your ssh key

```
# to copy and paste:
cat .ssh/id_rsa.pub
```

18. Add server IPv4 address to the hostname for now:

> 165.XXX.43.118

19. Create a dokku app:

```
dokku apps:create powerapp
```

20. Enable VHOST:

```
dokku domains:enable powerapp
```



**On Laptop**

21. Add dokku as a remote:

```
git remote add dokku dokku@165.XXX.43.118:powerapp
```

22. Verify that the remote got added:

```
git remote -v
```

23. Push it up (for every new change just run these commands):

```
git add .
git commit -m '🤞'
git push dokku master
```

24. Hit the server address (`165.XXX.43.118`) to make sure it works!



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
