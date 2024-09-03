```shell
# generate private key:
openssl genrsa -out private.pem 2048
```

```shell
# generate public key from private key
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
```