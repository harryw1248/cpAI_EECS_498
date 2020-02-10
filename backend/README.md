# Backend

## To install:

```sh
> source setup.sh
```

### Just remove `env` folder to reset your python environment.

```sh
> rm -rf env
> source setup.sh
```

## Deployment

**The best way to deploy a Flask app is by using Elastic Beanstalk CLI**

However, as a temporary solution, you can simply zip the code + config files and upload the zip file directly to AWS.

### Prepare a zip to upload to Elastic Beanstalk

_It's really important that run `zip.sh` wihin your python environment so that requirements.txt (which lists required Python packages/dependencies) is properly generated_

```sh
> source env/bin/activate
> ./zip.sh
```

Simply upload `app.zip` by clicking on `upload and deploy` -
<img src="./awseb.png"></img>
