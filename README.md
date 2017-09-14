## Export google cloud infrastructure into Terraform configs

* `pip install -r requirements.txt`
* `export TOKEN=$(gcloud config config-helper --format='value(credential.access_token)')`
* `export PROJECT=infra-13120`


*export compute instances:*
* `python resources/compute_instance.py config > main.tf`
* `python resources/compute_instance.py state > terraform.tfstate`

*export firewall rules:*
* `python resources/compute_instance.py state`
* `python resources/compute_instance.py config > firewall.tf`

Check with
```bash
$ terraform init # download google provider module
$ terraform plan
```

## Current problems with compute instances:
* Multiple ssh keys aren't handled properly and errors occur
* Tags aren't imported to state file

## Current problems with firewall rules:
* [deny](https://www.terraform.io/docs/providers/google/r/compute_firewall.html#deny) is still in beta and rules aren't imported properly to state file.
* EGRESS rules aren't supported at this time
