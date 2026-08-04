# OpenAlex ClickHouse validation — stage1

Local engine verdict: pass

Capacity verdict: Uncertain

## Input and environment identity

```json
{
  "environment": {
    "binfmt_registrations": "",
    "container_architecture": "aarch64",
    "container_cpuinfo": "processor\t: 0\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 1\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 2\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 3\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 4\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 5\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 6\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 7\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 8\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 9\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 10\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 11\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 12\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 13\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 14\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 15\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0",
    "docker_server_architecture": "aarch64",
    "host_architecture": "arm64",
    "image": "clickhouse/clickhouse-server:26.3.12.3",
    "image_architecture": "arm64",
    "image_id": "sha256:b76fe13844679c04c28354a4d12c4ec8b242b51d05abadb176c8adbe1187d5ad",
    "published_hosts": {
      "8123": "127.0.0.1",
      "9000": "127.0.0.1"
    },
    "raw_mount_read_only": true,
    "repo_digests": [
      "clickhouse/clickhouse-server@sha256:1f7cd090d5c4e2b8bfe0ea5d8ae6125937e1d932c6371b4d25fbd6088829dc9c"
    ],
    "resource_limits": {
      "memory_bytes": 34359738368,
      "nano_cpus": 16000000000
    }
  },
  "inputs": {
    "entity_manifests": {
      "institutions": {
        "content_length": 27023,
        "date": "2026-06-26",
        "etag": "\"5a48249e664d77d1d4aa8b050bb56f53\"",
        "last_modified": "Sat, 27 Jun 2026 03:06:32 GMT",
        "retrieved_at": "2026-08-04T19:03:34.299979+00:00",
        "sha256": "631a5521b1344ec8d08a8eef484a703e41eaedb94d524cebcf3697519f8f33c0",
        "url": "https://openalex.s3.amazonaws.com/data/parquet/institutions/manifest.json"
      },
      "works": {
        "content_length": 477208,
        "date": "2026-06-26",
        "etag": "\"9edf1873de62a74e25ff3d41e0124bbd\"",
        "last_modified": "Sat, 27 Jun 2026 03:04:38 GMT",
        "retrieved_at": "2026-08-04T19:03:34.251924+00:00",
        "sha256": "4b5142cb47f22fb5f6e91fc330ed800e355e8bb9421b10d812394780b9a1443d",
        "url": "https://openalex.s3.amazonaws.com/data/parquet/works/manifest.json"
      }
    },
    "expected_work_rows": 751167,
    "seed_work_ids": [
      73384,
      1709267,
      4412559786
    ],
    "selection_algorithm": "cumulative-bytes-four-strata-v2",
    "selection_sha256": "ccc7b5c51f04bd5972e6fb513f15157c13a79300be5fc5c36696aebbf56026b1",
    "stage1_coverage_policy": {
      "bias_caveat": "Stage 1 seeds each stratum with a file no larger than one quarter of its target. This size conditioning favors smaller files and makes Stage 1 a correctness sample, not a representative performance sample.",
      "cap_derivation": "floor(first_tier_target_bytes / 4)",
      "max_seed_file_bytes": 268435456,
      "scope": "first tier only",
      "strata": {
        "0": {
          "eligible_files": 666,
          "seed_file": {
            "content_length": 179823279,
            "rank": "007181ae8c1a708f1e0b5dbba3fea658f9ef301ed167a726ddfc2e601f366f83",
            "record_count": 144900,
            "stratum": 0,
            "updated_date": "2025-11-06",
            "url": "s3://openalex/data/parquet/works/updated_date=2025-11-06/part_0533.parquet"
          },
          "total_files": 966
        },
        "1": {
          "eligible_files": 479,
          "seed_file": {
            "content_length": 180571561,
            "rank": "0094a5d5f3009fc883b3b7fa6d711a68c0fdf0c5eb1afafc3010b2ae4927c530",
            "record_count": 145249,
            "stratum": 1,
            "updated_date": "2025-11-06",
            "url": "s3://openalex/data/parquet/works/updated_date=2025-11-06/part_0554.parquet"
          },
          "total_files": 712
        },
        "2": {
          "eligible_files": 113,
          "seed_file": {
            "content_length": 133103054,
            "rank": "01e130cb0d167e88731486e5807c6736ee94c1113f540bd2c6bbc653fd2097b6",
            "record_count": 221918,
            "stratum": 2,
            "updated_date": "2026-04-15",
            "url": "s3://openalex/data/parquet/works/updated_date=2026-04-15/part_0000.parquet"
          },
          "total_files": 464
        },
        "3": {
          "eligible_files": 32,
          "seed_file": {
            "content_length": 12522914,
            "rank": "0666cc03695dc4760751e58639e40731d6795226845303f5fbe7c353f06eee5d",
            "record_count": 4111,
            "stratum": 3,
            "updated_date": "2026-06-19",
            "url": "s3://openalex/data/parquet/works/updated_date=2026-06-19/part_0015.parquet"
          },
          "total_files": 304
        }
      },
      "tier": "stage1"
    }
  }
}
```

## Correctness

```json
{
  "build_hashes": [
    "e53efd856fbfacc5db9f247e4e3b4591d3e7fb017e7d5a9c4850d6533c1ef012",
    "e53efd856fbfacc5db9f247e4e3b4591d3e7fb017e7d5a9c4850d6533c1ef012"
  ],
  "gates": [
    {
      "actual": 751167,
      "blocking": true,
      "evidence": {
        "query": "raw_work_rows"
      },
      "expected": 751167,
      "name": "manifest_rows_match_parquet",
      "passed": true
    },
    {
      "actual": 751167,
      "blocking": true,
      "evidence": {
        "query": "raw_work_rows"
      },
      "expected": 751167,
      "name": "raw_work_ids_are_unique",
      "passed": true
    },
    {
      "actual": 0,
      "blocking": true,
      "evidence": {
        "raw_evidence": {
          "distinct_valid_pairs": 6689858,
          "duplicate_pair_delta": 0,
          "null_topic_scores": 0,
          "raw_reference_entries": 6689858,
          "rejected_id_entries": 0
        }
      },
      "expected": 0,
      "name": "raw_reference_ids_parse",
      "passed": true
    },
    {
      "actual": 0,
      "blocking": true,
      "evidence": {
        "raw_evidence": {
          "distinct_valid_pairs": 6689858,
          "duplicate_pair_delta": 0,
          "null_topic_scores": 0,
          "raw_reference_entries": 6689858,
          "rejected_id_entries": 0
        }
      },
      "expected": 0,
      "name": "topic_scores_are_non_null",
      "passed": true
    },
    {
      "actual": 1521028,
      "blocking": true,
      "evidence": {
        "raw_query": "raw_bridge_counts",
        "table_query": "materialized_counts"
      },
      "expected": 1521028,
      "name": "authors_bridge_reconciles",
      "passed": true
    },
    {
      "actual": 1191790,
      "blocking": true,
      "evidence": {
        "raw_query": "raw_bridge_counts",
        "table_query": "materialized_counts"
      },
      "expected": 1191790,
      "name": "institutions_bridge_reconciles",
      "passed": true
    },
    {
      "actual": 1340113,
      "blocking": true,
      "evidence": {
        "raw_query": "raw_bridge_counts",
        "table_query": "materialized_counts"
      },
      "expected": 1340113,
      "name": "topics_bridge_reconciles",
      "passed": true
    },
    {
      "actual": 6689858,
      "blocking": true,
      "evidence": {
        "duplicate_pair_delta": 0
      },
      "expected": 6689858,
      "name": "citation_pairs_reconcile",
      "passed": true
    },
    {
      "actual": 0,
      "blocking": true,
      "evidence": {
        "query": "referential_coverage"
      },
      "expected": 0,
      "name": "missing_works_for_authors",
      "passed": true
    },
    {
      "actual": 0,
      "blocking": true,
      "evidence": {
        "query": "referential_coverage"
      },
      "expected": 0,
      "name": "missing_authors",
      "passed": true
    },
    {
      "actual": 0,
      "blocking": true,
      "evidence": {
        "query": "referential_coverage"
      },
      "expected": 0,
      "name": "missing_topics",
      "passed": true
    },
    {
      "actual": 1513,
      "blocking": false,
      "evidence": {
        "distinct_missing_ids": 107,
        "query": "referential_coverage",
        "sample_query": "missing_institution_sample"
      },
      "expected": 0,
      "name": "missing_institutions",
      "passed": false
    },
    {
      "actual": 751167,
      "blocking": true,
      "evidence": {
        "query": "works_id_uniqueness"
      },
      "expected": 751167,
      "name": "works_ids_are_unique",
      "passed": true
    },
    {
      "actual": 1172764,
      "blocking": true,
      "evidence": {
        "query": "authors_id_uniqueness"
      },
      "expected": 1172764,
      "name": "authors_ids_are_unique",
      "passed": true
    },
    {
      "actual": 127784,
      "blocking": true,
      "evidence": {
        "query": "institutions_id_uniqueness"
      },
      "expected": 127784,
      "name": "institutions_ids_are_unique",
      "passed": true
    },
    {
      "actual": 283287,
      "blocking": true,
      "evidence": {
        "query": "sources_id_uniqueness"
      },
      "expected": 283287,
      "name": "sources_ids_are_unique",
      "passed": true
    },
    {
      "actual": 4516,
      "blocking": true,
      "evidence": {
        "query": "topics_id_uniqueness"
      },
      "expected": 4516,
      "name": "topics_ids_are_unique",
      "passed": true
    }
  ],
  "missing_institution_sample": [
    {
      "display_name": "Tampere University",
      "institution_id": 4210133110,
      "raw_bridge_rows": 322
    },
    {
      "display_name": "Southwestern Medical Center",
      "institution_id": 4210096815,
      "raw_bridge_rows": 234
    },
    {
      "display_name": "National Yang Ming Chiao Tung University",
      "institution_id": 96323854,
      "raw_bridge_rows": 80
    },
    {
      "display_name": "North West Agriculture and Forestry University",
      "institution_id": 4210088176,
      "raw_bridge_rows": 76
    },
    {
      "display_name": "University of Clermont Auvergne",
      "institution_id": 4210103002,
      "raw_bridge_rows": 65
    },
    {
      "display_name": "University of Campania \"Luigi Vanvitelli\"",
      "institution_id": 4210126337,
      "raw_bridge_rows": 53
    },
    {
      "display_name": "The University of Texas Health Science Center",
      "institution_id": 4210159031,
      "raw_bridge_rows": 45
    },
    {
      "display_name": "Institut Agro Montpelier",
      "institution_id": 4210136436,
      "raw_bridge_rows": 43
    },
    {
      "display_name": "Seattle Children's Hospital",
      "institution_id": 4210109034,
      "raw_bridge_rows": 41
    },
    {
      "display_name": "Department of Biomedicine Basel",
      "institution_id": 4210128905,
      "raw_bridge_rows": 33
    },
    {
      "display_name": "Federal University of S\u00e3o Jo\u00e3o del-Rei",
      "institution_id": 4210130985,
      "raw_bridge_rows": 30
    },
    {
      "display_name": "Universit\u00e9 Paul-Val\u00e9ry Montpellier",
      "institution_id": 4210095130,
      "raw_bridge_rows": 24
    },
    {
      "display_name": "ZHAW Zurich University of Applied Sciences",
      "institution_id": 200744771,
      "raw_bridge_rows": 21
    },
    {
      "display_name": "Parul University",
      "institution_id": 4210112983,
      "raw_bridge_rows": 21
    },
    {
      "display_name": "Toulouse Mathematics Institute",
      "institution_id": 4210098964,
      "raw_bridge_rows": 20
    },
    {
      "display_name": "Pontificial Catholic University of Valparaiso",
      "institution_id": 4210116133,
      "raw_bridge_rows": 20
    },
    {
      "display_name": "Texas A&M Health Science Center",
      "institution_id": 4210105967,
      "raw_bridge_rows": 19
    },
    {
      "display_name": "University of Management and Technology",
      "institution_id": 4210089805,
      "raw_bridge_rows": 15
    },
    {
      "display_name": "Office of the Assistant Secretary for Health",
      "institution_id": 4210113149,
      "raw_bridge_rows": 14
    },
    {
      "display_name": "Cracow University of Technology",
      "institution_id": 4210092770,
      "raw_bridge_rows": 13
    },
    {
      "display_name": "Iscte \u2013 Instituto Universit\u00e1rio de Lisboa",
      "institution_id": 4210100009,
      "raw_bridge_rows": 13
    },
    {
      "display_name": "Franciscan University",
      "institution_id": 4210115425,
      "raw_bridge_rows": 13
    },
    {
      "display_name": "Beibu Gulf University",
      "institution_id": 4210128032,
      "raw_bridge_rows": 13
    },
    {
      "display_name": "Lurie Children's Hospital",
      "institution_id": 4210125713,
      "raw_bridge_rows": 12
    },
    {
      "display_name": "Indonesia Open University",
      "institution_id": 4210132268,
      "raw_bridge_rows": 12
    }
  ],
  "raw_evidence": {
    "distinct_valid_pairs": 6689858,
    "duplicate_pair_delta": 0,
    "null_topic_scores": 0,
    "raw_reference_entries": 6689858,
    "rejected_id_entries": 0
  },
  "rebuild_deterministic": true,
  "referential_coverage": {
    "authors_with_missing_institutions": 1468,
    "citation_edges": 6689858,
    "citation_retention_ratio": 0.0024964655453075385,
    "distinct_missing_institution_ids": 107,
    "distinct_missing_topic_ids": 0,
    "institution_bridge_rows": 1191790,
    "institution_reference_coverage_ratio": 0.998730481041123,
    "missing_authors": 0,
    "missing_institutions": 1513,
    "missing_topics": 0,
    "missing_works_for_authors": 0,
    "retained_cited_edges": 16701,
    "topic_bridge_rows": 1340113,
    "topic_reference_coverage_ratio": 1,
    "works_with_missing_institutions": 718
  }
}
```

## Sequential and concurrent evidence

```json
{
  "concurrent": {
    "status": "not run in Stage 1"
  },
  "sequential": [
    {
      "elapsed_seconds": 0.066,
      "gating": true,
      "peak_memory_bytes": 62576874,
      "query_class": "routine",
      "query_id": "df512afc-6dbe-5945-a5d1-e55bf577bf44",
      "query_name": "q01",
      "read_bytes": 4507002,
      "read_rows": 751167,
      "result_rows": 4667,
      "run_kind": "post_restart_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.011,
      "gating": true,
      "peak_memory_bytes": 62959821,
      "query_class": "routine",
      "query_id": "daf2a53e-c750-5e2f-860b-e1505cfea366",
      "query_name": "q01",
      "read_bytes": 4507002,
      "read_rows": 751167,
      "result_rows": 4667,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.011,
      "gating": true,
      "peak_memory_bytes": 63673993,
      "query_class": "routine",
      "query_id": "d3bb4593-4c92-5135-a170-ffa8c6570ed0",
      "query_name": "q01",
      "read_bytes": 4507002,
      "read_rows": 751167,
      "result_rows": 4667,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.013,
      "gating": true,
      "peak_memory_bytes": 66745698,
      "query_class": "routine",
      "query_id": "5a32df48-5741-5587-ac89-9ce3aba1a9ab",
      "query_name": "q01",
      "read_bytes": 4507002,
      "read_rows": 751167,
      "result_rows": 4667,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.014,
      "gating": true,
      "peak_memory_bytes": 66730834,
      "query_class": "routine",
      "query_id": "e04f25c3-0733-5e23-9720-f93eefba728d",
      "query_name": "q01",
      "read_bytes": 4507002,
      "read_rows": 751167,
      "result_rows": 4667,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.015,
      "gating": true,
      "peak_memory_bytes": 68874962,
      "query_class": "routine",
      "query_id": "3f5f661e-7b16-5e6b-8061-a243b02826cf",
      "query_name": "q01",
      "read_bytes": 4507002,
      "read_rows": 751167,
      "result_rows": 4667,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.144,
      "gating": true,
      "peak_memory_bytes": 421420141,
      "query_class": "join",
      "query_id": "13595f55-8ce6-5f96-9afd-a4a8889d126a",
      "query_name": "q02",
      "read_bytes": 32921886,
      "read_rows": 2095796,
      "result_rows": 232103,
      "run_kind": "post_restart_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.099,
      "gating": true,
      "peak_memory_bytes": 400345834,
      "query_class": "join",
      "query_id": "a2848046-3ec2-5022-963e-ecd8f76e25e6",
      "query_name": "q02",
      "read_bytes": 32921886,
      "read_rows": 2095796,
      "result_rows": 232103,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.092,
      "gating": true,
      "peak_memory_bytes": 401837360,
      "query_class": "join",
      "query_id": "5504b261-1dca-5b3c-a586-47a9e9403c20",
      "query_name": "q02",
      "read_bytes": 32921886,
      "read_rows": 2095796,
      "result_rows": 232103,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.092,
      "gating": true,
      "peak_memory_bytes": 399989932,
      "query_class": "join",
      "query_id": "edd03e6a-5f6b-5a3c-9c5b-bc50f3eddaad",
      "query_name": "q02",
      "read_bytes": 32921886,
      "read_rows": 2095796,
      "result_rows": 232103,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.094,
      "gating": true,
      "peak_memory_bytes": 412161803,
      "query_class": "join",
      "query_id": "bfad4687-cb42-5ffe-bbec-e399dc66ffac",
      "query_name": "q02",
      "read_bytes": 32921886,
      "read_rows": 2095796,
      "result_rows": 232103,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.086,
      "gating": true,
      "peak_memory_bytes": 394931615,
      "query_class": "join",
      "query_id": "c63b7a6c-1bb7-5a2d-8f4b-edc4eb13fe71",
      "query_name": "q02",
      "read_bytes": 32921886,
      "read_rows": 2095796,
      "result_rows": 232103,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.115,
      "gating": true,
      "peak_memory_bytes": 910448132,
      "query_class": "join",
      "query_id": "55a2bf14-7bc6-50bb-b8f8-e7afc7b5a6d8",
      "query_name": "q03",
      "read_bytes": 63929729,
      "read_rows": 3444959,
      "result_rows": 1000,
      "run_kind": "post_restart_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.093,
      "gating": true,
      "peak_memory_bytes": 914494769,
      "query_class": "join",
      "query_id": "68b45e30-86bb-5487-9691-09331c63a648",
      "query_name": "q03",
      "read_bytes": 63929729,
      "read_rows": 3444959,
      "result_rows": 1000,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.097,
      "gating": true,
      "peak_memory_bytes": 914947333,
      "query_class": "join",
      "query_id": "c3ea97aa-7c10-5851-805d-648e39c76f4d",
      "query_name": "q03",
      "read_bytes": 63929729,
      "read_rows": 3444959,
      "result_rows": 1000,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.105,
      "gating": true,
      "peak_memory_bytes": 920682109,
      "query_class": "join",
      "query_id": "02ca305d-ad37-5cb1-a79a-a037ed6dc1df",
      "query_name": "q03",
      "read_bytes": 63929729,
      "read_rows": 3444959,
      "result_rows": 1000,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.105,
      "gating": true,
      "peak_memory_bytes": 923238708,
      "query_class": "join",
      "query_id": "5e44ed1a-1a6c-53c4-963f-15b1773e443c",
      "query_name": "q03",
      "read_bytes": 63929729,
      "read_rows": 3444959,
      "result_rows": 1000,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.094,
      "gating": true,
      "peak_memory_bytes": 915522101,
      "query_class": "join",
      "query_id": "940ad897-60ba-5c49-9760-e4c1df1d7253",
      "query_name": "q03",
      "read_bytes": 63929729,
      "read_rows": 3444959,
      "result_rows": 1000,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.177,
      "gating": true,
      "peak_memory_bytes": 370622987,
      "query_class": "join",
      "query_id": "7ba2143e-1129-5b61-aa62-5815d203c396",
      "query_name": "q04",
      "read_bytes": 51228561,
      "read_rows": 3390315,
      "result_rows": 35542,
      "run_kind": "post_restart_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.146,
      "gating": true,
      "peak_memory_bytes": 374519006,
      "query_class": "join",
      "query_id": "cedb075c-63d5-5b0e-95b3-395ba6ca4d9a",
      "query_name": "q04",
      "read_bytes": 51228561,
      "read_rows": 3390315,
      "result_rows": 35542,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.144,
      "gating": true,
      "peak_memory_bytes": 371685996,
      "query_class": "join",
      "query_id": "9801aa14-b9e6-5fd2-b51f-036a8ddf9c9a",
      "query_name": "q04",
      "read_bytes": 51228561,
      "read_rows": 3390315,
      "result_rows": 35542,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.145,
      "gating": true,
      "peak_memory_bytes": 370313980,
      "query_class": "join",
      "query_id": "cac9576c-5bbd-5797-b028-2d781cf4f7c1",
      "query_name": "q04",
      "read_bytes": 51228561,
      "read_rows": 3390315,
      "result_rows": 35542,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.147,
      "gating": true,
      "peak_memory_bytes": 386769528,
      "query_class": "join",
      "query_id": "0810c65e-2c98-5cd1-b43c-bfb4c95a789a",
      "query_name": "q04",
      "read_bytes": 51228561,
      "read_rows": 3390315,
      "result_rows": 35542,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.143,
      "gating": true,
      "peak_memory_bytes": 385615817,
      "query_class": "join",
      "query_id": "3b30e5aa-2e1a-5868-8c48-f7db737325cd",
      "query_name": "q04",
      "read_bytes": 51228561,
      "read_rows": 3390315,
      "result_rows": 35542,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.029,
      "gating": true,
      "peak_memory_bytes": 548632,
      "query_class": "one_hop",
      "query_id": "b730b9c4-9614-57b4-b429-efae8d8cca95",
      "query_name": "q05",
      "read_bytes": 53649936,
      "read_rows": 6706242,
      "result_rows": 0,
      "run_kind": "post_restart_run",
      "seed_work_id": 73384,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.012,
      "gating": true,
      "peak_memory_bytes": 765550,
      "query_class": "one_hop",
      "query_id": "4c447197-0298-5dcc-863c-bb68268e94b7",
      "query_name": "q05",
      "read_bytes": 53719384,
      "read_rows": 6706242,
      "result_rows": 51,
      "run_kind": "warm_run",
      "seed_work_id": 1709267,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.012,
      "gating": true,
      "peak_memory_bytes": 763103,
      "query_class": "one_hop",
      "query_id": "cecc163f-7a64-5b1a-8a6b-67432d383cf3",
      "query_name": "q05",
      "read_bytes": 53745640,
      "read_rows": 6706242,
      "result_rows": 2545,
      "run_kind": "warm_run",
      "seed_work_id": 4412559786,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.001,
      "gating": true,
      "peak_memory_bytes": 315440,
      "query_class": "one_hop",
      "query_id": "56847c14-8888-5648-b76e-e6bcc1efb0fe",
      "query_name": "q05",
      "read_bytes": 0,
      "read_rows": 0,
      "result_rows": 0,
      "run_kind": "warm_run",
      "seed_work_id": 73384,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.002,
      "gating": true,
      "peak_memory_bytes": 352958,
      "query_class": "one_hop",
      "query_id": "05433fc9-a0fd-5105-a0bf-222b56ccdaee",
      "query_name": "q05",
      "read_bytes": 200520,
      "read_rows": 16384,
      "result_rows": 51,
      "run_kind": "warm_run",
      "seed_work_id": 1709267,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.002,
      "gating": true,
      "peak_memory_bytes": 412270,
      "query_class": "one_hop",
      "query_id": "4d1ec754-13eb-50d6-a22c-98ed007e69a9",
      "query_name": "q05",
      "read_bytes": 226776,
      "read_rows": 16384,
      "result_rows": 2545,
      "run_kind": "warm_run",
      "seed_work_id": 4412559786,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.004,
      "gating": false,
      "peak_memory_bytes": 478232,
      "query_class": "two_hop",
      "query_id": "e3fe4ac0-fa86-5a02-8efd-25c540966369",
      "query_name": "q06",
      "read_bytes": 131072,
      "read_rows": 16384,
      "result_rows": 1,
      "run_kind": "post_restart_run",
      "seed_work_id": 73384,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.024,
      "gating": false,
      "peak_memory_bytes": 5001249,
      "query_class": "two_hop",
      "query_id": "9d2e2953-22dd-5b31-b4e5-9cf8066454f2",
      "query_name": "q06",
      "read_bytes": 107238248,
      "read_rows": 6706242,
      "result_rows": 1,
      "run_kind": "warm_run",
      "seed_work_id": 1709267,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.018,
      "gating": false,
      "peak_memory_bytes": 4038766,
      "query_class": "two_hop",
      "query_id": "31906d93-f6aa-506e-9e0d-98386489f28e",
      "query_name": "q06",
      "read_bytes": 107264504,
      "read_rows": 6706242,
      "result_rows": 1,
      "run_kind": "warm_run",
      "seed_work_id": 4412559786,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.003,
      "gating": false,
      "peak_memory_bytes": 467312,
      "query_class": "two_hop",
      "query_id": "8be06a02-9757-5ba0-b974-acaa423bac3f",
      "query_name": "q06",
      "read_bytes": 131072,
      "read_rows": 16384,
      "result_rows": 1,
      "run_kind": "warm_run",
      "seed_work_id": 73384,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.017,
      "gating": false,
      "peak_memory_bytes": 3801559,
      "query_class": "two_hop",
      "query_id": "ca252312-d31a-51f9-97b5-8e8957b9d0f9",
      "query_name": "q06",
      "read_bytes": 107238248,
      "read_rows": 6706242,
      "result_rows": 1,
      "run_kind": "warm_run",
      "seed_work_id": 1709267,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.018,
      "gating": false,
      "peak_memory_bytes": 4415075,
      "query_class": "two_hop",
      "query_id": "06e16dca-0cb0-5a21-a590-9ab54e9aecf3",
      "query_name": "q06",
      "read_bytes": 107264504,
      "read_rows": 6706242,
      "result_rows": 1,
      "run_kind": "warm_run",
      "seed_work_id": 4412559786,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.097,
      "gating": true,
      "peak_memory_bytes": 417740601,
      "query_class": "routine",
      "query_id": "98beb1b8-f4dc-5c3f-8698-b25017f646c8",
      "query_name": "q07",
      "read_bytes": 73588438,
      "read_rows": 6689858,
      "result_rows": 1000,
      "run_kind": "post_restart_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.067,
      "gating": true,
      "peak_memory_bytes": 430933682,
      "query_class": "routine",
      "query_id": "8f02c1e1-b7c5-5c70-90de-d5aac44f331b",
      "query_name": "q07",
      "read_bytes": 73588438,
      "read_rows": 6689858,
      "result_rows": 1000,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.062,
      "gating": true,
      "peak_memory_bytes": 427538793,
      "query_class": "routine",
      "query_id": "58755398-ae4b-5258-8d79-71348767369e",
      "query_name": "q07",
      "read_bytes": 73588438,
      "read_rows": 6689858,
      "result_rows": 1000,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.066,
      "gating": true,
      "peak_memory_bytes": 421948078,
      "query_class": "routine",
      "query_id": "ca0b271f-58da-5e7a-ae72-b5fb29797641",
      "query_name": "q07",
      "read_bytes": 73588438,
      "read_rows": 6689858,
      "result_rows": 1000,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.066,
      "gating": true,
      "peak_memory_bytes": 422068191,
      "query_class": "routine",
      "query_id": "590f6f1c-a94f-543d-9cc9-292c8eca5018",
      "query_name": "q07",
      "read_bytes": 73588438,
      "read_rows": 6689858,
      "result_rows": 1000,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    },
    {
      "elapsed_seconds": 0.064,
      "gating": true,
      "peak_memory_bytes": 423277620,
      "query_class": "routine",
      "query_id": "37eecc92-ac52-54ae-8794-7f5398c6662d",
      "query_name": "q07",
      "read_bytes": 73588438,
      "read_rows": 6689858,
      "result_rows": 1000,
      "run_kind": "warm_run",
      "seed_work_id": null,
      "spill_bytes": 0
    }
  ]
}
```

## Storage and capacity evidence

```json
{
  "observed_peak_bytes": 1447362560,
  "samples": [
    {
      "filesystem_bytes": 1041252352,
      "projection_bytes": {},
      "table_bytes": {},
      "timestamp": 1785874632.023597
    },
    {
      "filesystem_bytes": 1140068352,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 41464778,
        "institutions": 4357308,
        "sources": 10677280,
        "topics": 150309,
        "works": 15247830
      },
      "timestamp": 1785874634.218254
    },
    {
      "filesystem_bytes": 1219780608,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 41464778,
        "citation_edge": 42958593,
        "institutions": 4357308,
        "sources": 10677280,
        "topics": 150309,
        "work_author": 15193249,
        "work_institution": 10501817,
        "work_topic": 12872189,
        "works": 15247830
      },
      "timestamp": 1785874636.185573
    },
    {
      "filesystem_bytes": 1220251648,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 41464778,
        "citation_edge": 42958593,
        "institutions": 4357308,
        "sources": 10677280,
        "topics": 150309,
        "work_author": 15193249,
        "work_institution": 10501817,
        "work_topic": 12872189,
        "works": 15247830
      },
      "timestamp": 1785874637.01018
    },
    {
      "filesystem_bytes": 1265422336,
      "projection_bytes": {},
      "table_bytes": {},
      "timestamp": 1785874642.034944
    },
    {
      "filesystem_bytes": 1352687616,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 41464778,
        "citation_edge": 16189782,
        "institutions": 4357308,
        "sources": 10677280,
        "topics": 150309,
        "works": 15247830
      },
      "timestamp": 1785874644.026527
    },
    {
      "filesystem_bytes": 1447362560,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 41464778,
        "citation_edge": 42958993,
        "institutions": 4357308,
        "sources": 10677280,
        "topics": 150309,
        "work_author": 15196343,
        "work_institution": 10513009,
        "work_topic": 12874656,
        "works": 15247830
      },
      "timestamp": 1785874645.6831539
    }
  ],
  "sampling_note": "Each build records an initial baseline and a forced final sample. Empty initial table_bytes means no active parts existed yet; empty projection_bytes means the SQL scripts executed by this Stage 1 build create no projections."
}
```

Scaling slopes are empirical evidence from sampled tiers; they are not a full-size prediction.

## Limitations

- Stage 1 validates correctness and query execution on a target of approximately 1 GiB; its actual size can exceed that target by one selected file.
- Stage 1 seeds each stratum with a file no larger than one quarter of its target. This size conditioning favors smaller files and makes Stage 1 a correctness sample, not a representative performance sample.
- Stage 1 scaling evidence is not a full-size prediction.
- The Docker Desktop VM has 48 GiB; the ClickHouse container is capped at 32 GiB. A 64-GiB Docker VM did not boot on this host.
- Only 16701 of 6689858 citation edges point to another Work inside this partial sample (retention ratio 0.002496); this is sampling-induced and is not evidence of citation data loss.
- The canonical Institutions snapshot does not resolve 1513 of 1191790 Work-institution bridge rows (107 distinct IDs; coverage ratio 0.998730). The raw links are preserved and analyses must use LEFT JOIN when unmatched affiliations matter.
