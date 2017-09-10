## Export google cloud infrastructure into Terraform configs

* `pip install -r requirements.txt`
* `export TOKEN=$(gcloud config config-helper --format='value(credential.access_token)')`
* `export PROJECT=infra-13120`
* `python resources/compute_instance.py config > main.tf`
* `python resources/compute_instance.py state > terraform.tfstate`

Check with
```bash
$ terraform plan
```
