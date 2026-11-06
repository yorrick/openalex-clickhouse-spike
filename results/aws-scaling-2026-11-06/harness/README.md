# Experimental harness archive

These files archive the study scripts and guest payloads for provenance. The original execution directory is `~/work/data/openalex-tier-scaling-20261106/`, with the legacy lifecycle under the sibling `openalex-small-spike-20261105/`. Guest code imports the repository at commit `0b3d5bcfbb5062aca4d26ae5f813c4659a234b5d`. This archive preserves the original directory assumptions and is not an unattended deployment entry point.

The 2m/10m guest was extracted from deployed user data; the 31m baseline disables the optional resource variants, leaving the primary path unchanged. The current controller adds an expected-AMI rejection for the tuning run. The tuning guest runs the exact five-case loop on a three-Work native fixture before loading 31.9m Works. No abandoned generic resource-variant draft is included.

`input-files.json` one level above maps public OpenAlex object keys, VersionIds, byte counts, Parquet row counts and SHA256 fingerprints to the three cohort manifests. Raw input payloads are not committed. Compressed telemetry files preserve complete timing/monitoring records, including query CPU counters, memory samples and diskstat endpoints and intermediate samples. Aggregate outputs and QA SHA256 hashes are in the tier JSON files.

Running these scripts creates billable AWS resources and requires the original manifest/state files and certification SSO setup. The completed run required no raw input upload from the laptop. Source and result buckets have separate retention; the raw EBS volume is deliberately retained. No full-corpus run was performed.
