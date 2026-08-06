# OpenAlex ClickHouse validation — stage2-repeat-medium-18c18t-r2

Local engine verdict: pass

Capacity verdict: Uncertain

## Input and environment identity

```json
{
  "environment": {
    "binfmt_registrations": "",
    "container_architecture": "aarch64",
    "container_cpuinfo": "processor\t: 0\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 1\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 2\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 3\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 4\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 5\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 6\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 7\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 8\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 9\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 10\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 11\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 12\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 13\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 14\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 15\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 16\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 17\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0",
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
      "docker_cpus": 18,
      "docker_memory_bytes": 58864549888,
      "memory_bytes": 53687091200,
      "nano_cpus": 17999998976
    }
  },
  "inputs": {
    "complete_authors_bytes": 52769910496,
    "maximum_raw_input_bytes": 98301763421,
    "run_identity": {
      "config_sha256": "f30f5dc8ff0d754e60a9bddb803e8d91d249e262ce077766939744e13853e818",
      "download_state_sha256": "c01aa4ecf6f9b005eb14120b6de797a3e70a2c727a5e15254b6f6a8ef11a939e",
      "execution": {
        "cpus": 18,
        "maximum_seconds": 18000,
        "query_threads": 18,
        "workers": 1
      },
      "identity_version": 2,
      "memory_gib": 50,
      "rendered_sql_sha256": {
        "00_schema.sql": "5ab5168ebbcf957b5b807bcdd89c08d7ab07575cf11236653e550c6f0d0a5e1f",
        "11_load_complete_authors.sql": "3cabd09ab9e2a68b70348f0cabc215e7ea395643385b0a4aa32917679c491c33",
        "12_load_small_dimensions.sql": "c43593c943cfdc0176c07d4e7752b43872b2d20ebe093c8a137f577aebc91619",
        "30_reverse_projection.sql": "8757b9574cb94232061ba73dfaf0c0f3d9cac764ba144b52c719d0210e8d3d96",
        "stage2_medium/05_raw_evidence.sql": "486472a3a3a3ec5a2b11d965c4933a6bce4c1bd35dbdb31fe2d694f1c8d40e5a",
        "stage2_medium/20_load_works.sql": "c139806aee59508383590b850f2e4178200d02e0cd30c177684d41236effdd5f"
      },
      "run_id": "stage2-repeat-medium-18c18t-r2",
      "selection_sha256": "ccc7b5c51f04bd5972e6fb513f15157c13a79300be5fc5c36696aebbf56026b1",
      "sha256": "da0cb6476b4783e7d28b88e16908bfed0c53cf7ccf9bc9e0c3755ca99cdbe8ef",
      "tiers": [
        "stage2_medium"
      ]
    },
    "seed_work_ids": [
      25441,
      1491165,
      4388957908
    ],
    "selection_algorithm": "cumulative-bytes-four-strata-v2",
    "selection_sha256": "ccc7b5c51f04bd5972e6fb513f15157c13a79300be5fc5c36696aebbf56026b1",
    "tiers": {
      "stage2_medium": {
        "content_length": 15118229383,
        "record_count": 10109733
      }
    }
  }
}
```

## Correctness

```json
{
  "stage2_medium": {
    "distribution_digests": {
      "authorships_per_work": {
        "item_count": 447,
        "sha256": "2bc843d8da3f9998d26c7d558b7c8464e08af5a43f8e0128f60d3aa4c3f77d9e",
        "value_kind": "rows"
      },
      "materialized_counts": {
        "item_count": 5,
        "sha256": "c7cb5044f5ae88ebb494ae9f013a9beaea31a1a8bf879c680f5843901b501295",
        "value_kind": "object"
      },
      "missing_author_sample": {
        "item_count": 25,
        "sha256": "2029b08cef3cc2b317e2e92a98c1c91cfbed1f75ef27fafca4b6a895f7c9fc95",
        "value_kind": "rows"
      },
      "missing_institution_sample": {
        "item_count": 25,
        "sha256": "041d556c79b9cc31f860bd11a2eb21e1f96d47e8e9ce9c80b50b2f84fd9f03c5",
        "value_kind": "rows"
      },
      "referential_coverage": {
        "item_count": 26,
        "sha256": "fdc73192483ebb54d8e94660e9c417dae234a3e725cbd345d34b86df26212b1e",
        "value_kind": "object"
      },
      "year_type_topic_xpac": {
        "item_count": 1307378,
        "sha256": "9fd1a41a5f5bc8119582c700239d950531afec5124792c9998806df498e7da42",
        "value_kind": "rows"
      }
    },
    "gates": [
      {
        "actual": 10109733,
        "blocking": true,
        "evidence": {
          "query": "raw_work_rows"
        },
        "expected": 10109733,
        "name": "manifest_rows_match_parquet",
        "passed": true
      },
      {
        "actual": 10109733,
        "blocking": true,
        "evidence": {
          "query": "raw_work_rows"
        },
        "expected": 10109733,
        "name": "raw_work_ids_are_unique",
        "passed": true
      },
      {
        "actual": 0,
        "blocking": true,
        "evidence": {
          "raw_evidence": {
            "distinct_valid_pairs": 70415984,
            "duplicate_pair_delta": 0,
            "null_topic_scores": 0,
            "raw_reference_entries": 70415984,
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
            "distinct_valid_pairs": 70415984,
            "duplicate_pair_delta": 0,
            "null_topic_scores": 0,
            "raw_reference_entries": 70415984,
            "rejected_id_entries": 0
          }
        },
        "expected": 0,
        "name": "topic_scores_are_non_null",
        "passed": true
      },
      {
        "actual": 16075482,
        "blocking": true,
        "evidence": {
          "raw_query": "raw_bridge_counts",
          "table_query": "materialized_counts"
        },
        "expected": 16075482,
        "name": "authors_bridge_reconciles",
        "passed": true
      },
      {
        "actual": 12517247,
        "blocking": true,
        "evidence": {
          "raw_query": "raw_bridge_counts",
          "table_query": "materialized_counts"
        },
        "expected": 12517247,
        "name": "institutions_bridge_reconciles",
        "passed": true
      },
      {
        "actual": 21657004,
        "blocking": true,
        "evidence": {
          "raw_query": "raw_bridge_counts",
          "table_query": "materialized_counts"
        },
        "expected": 21657004,
        "name": "topics_bridge_reconciles",
        "passed": true
      },
      {
        "actual": 70415984,
        "blocking": true,
        "evidence": {
          "duplicate_pair_delta": 0
        },
        "expected": 70415984,
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
        "name": "missing_topics",
        "passed": true
      },
      {
        "actual": 33354,
        "blocking": false,
        "evidence": {
          "affected_works": 33242,
          "deleted_author_rows": 0,
          "distinct_missing_ids": 238,
          "null_author_rows": 33089,
          "overall_coverage": 0.9979251633014798,
          "query": "referential_coverage",
          "sample_query": "missing_author_sample",
          "special_author_documentation": "https://help.openalex.org/hc/en-us/articles/28763618477975-Why-are-some-authors-assigned-to-NULL-AUTHOR-ID-A9999999999",
          "special_author_ids": [
            9999999999,
            5317838346
          ]
        },
        "expected": 0,
        "name": "missing_authors",
        "passed": false
      },
      {
        "actual": 0.9999834812674144,
        "blocking": true,
        "evidence": {
          "affected_works": 198,
          "distinct_ordinary_missing_ids": 237,
          "excluded_special_author_ids": [
            9999999999,
            5317838346
          ],
          "ordinary_authorship_rows": 16042393,
          "ordinary_missing_rows": 265,
          "query": "referential_coverage",
          "zero_denominator_convention": "coverage is 1 only when ordinary_authorship_rows is zero; authors_bridge_reconciles independently pins total bridge rows"
        },
        "expected": ">=0.999000",
        "name": "ordinary_author_reference_coverage",
        "passed": true
      },
      {
        "actual": 14602,
        "blocking": false,
        "evidence": {
          "distinct_missing_ids": 134,
          "query": "referential_coverage",
          "sample_query": "missing_institution_sample"
        },
        "expected": 0,
        "name": "missing_institutions",
        "passed": false
      },
      {
        "actual": 10109733,
        "blocking": true,
        "evidence": {
          "query": "works_id_uniqueness"
        },
        "expected": 10109733,
        "name": "works_ids_are_unique",
        "passed": true
      },
      {
        "actual": 119129660,
        "blocking": true,
        "evidence": {
          "query": "authors_id_uniqueness"
        },
        "expected": 119129660,
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
    "missing_author_sample": [
      {
        "author_id": 9999999999,
        "classification": "null_author",
        "display_names": [
          "",
          "\"Jos\u00e9 Francisco Vald\u00e9s-Galicia\"",
          "\"Lukas Einkemmer\"",
          "\"Ralf Kissmann\"",
          "\"The CIA's Hidden War.\""
        ],
        "raw_bridge_rows": 33089
      },
      {
        "author_id": 5013217494,
        "classification": "ordinary",
        "display_names": [
          "F. Xavier Medina",
          "Francesc-Xavier Medina"
        ],
        "raw_bridge_rows": 6
      },
      {
        "author_id": 5063807156,
        "classification": "ordinary",
        "display_names": [
          "Diego Redolar",
          "Diego Redolar Ripoll",
          "Diego Redolar-Ripoll"
        ],
        "raw_bridge_rows": 5
      },
      {
        "author_id": 5015883457,
        "classification": "ordinary",
        "display_names": [
          "Porter, SR"
        ],
        "raw_bridge_rows": 4
      },
      {
        "author_id": 5108107655,
        "classification": "ordinary",
        "display_names": [
          "Jos\u00e9 Brandariz",
          "Jos\u00e9 \u00c1ngel Brandariz",
          "Jos\u00e9 \u00c1ngel Brandariz Garc\u00eda"
        ],
        "raw_bridge_rows": 4
      },
      {
        "author_id": 5083729552,
        "classification": "ordinary",
        "display_names": [
          "Cristina Pujol",
          "Universitat Oberta de Catalunya"
        ],
        "raw_bridge_rows": 3
      },
      {
        "author_id": 5101601348,
        "classification": "ordinary",
        "display_names": [
          "A. Martelli",
          "Martelli, A."
        ],
        "raw_bridge_rows": 3
      },
      {
        "author_id": 5014983459,
        "classification": "ordinary",
        "display_names": [
          "Gomes, Maria Elisa Preto"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5031019573,
        "classification": "ordinary",
        "display_names": [
          "Nasir, ZA",
          "Nasir,\u00a0ZA"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5034986435,
        "classification": "ordinary",
        "display_names": [
          "Elisenda Ard\u00e8vol",
          "Elisenda Ard\u00e8vol Piera"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5041415886,
        "classification": "ordinary",
        "display_names": [
          "Poulsen, Niels Kj\u00f8lstad"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5074326473,
        "classification": "ordinary",
        "display_names": [
          "Borja Martinez",
          "Martinez, Borja"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5080662145,
        "classification": "ordinary",
        "display_names": [
          "ISIDORI, Andrea"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5099632339,
        "classification": "ordinary",
        "display_names": [
          "Zygmunt Bauman"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5099632340,
        "classification": "ordinary",
        "display_names": [
          "Prof Tim May"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5115575883,
        "classification": "ordinary",
        "display_names": [
          "Acad\u00e9mie nationale de m\u00e9decine"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5001400935,
        "classification": "ordinary",
        "display_names": [
          "Cecillon, L."
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5001448296,
        "classification": "ordinary",
        "display_names": [
          "Hagopian, S"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5002485218,
        "classification": "ordinary",
        "display_names": [
          "Copin, Y."
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5003024816,
        "classification": "ordinary",
        "display_names": [
          "Lamers, C."
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5004335124,
        "classification": "ordinary",
        "display_names": [
          "Kurki-Suonio, H."
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5004399630,
        "classification": "ordinary",
        "display_names": [
          "F. Etienne"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5004495876,
        "classification": "ordinary",
        "display_names": [
          "Abdoulaye, Tahirou"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5004822510,
        "classification": "ordinary",
        "display_names": [
          "Carvalho, W"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5005191039,
        "classification": "ordinary",
        "display_names": [
          "Chollet, Franck"
        ],
        "raw_bridge_rows": 1
      }
    ],
    "missing_institution_sample": [
      {
        "display_name": "Tampere University",
        "institution_id": 4210133110,
        "raw_bridge_rows": 3208
      },
      {
        "display_name": "Southwestern Medical Center",
        "institution_id": 4210096815,
        "raw_bridge_rows": 2069
      },
      {
        "display_name": "National Yang Ming Chiao Tung University",
        "institution_id": 96323854,
        "raw_bridge_rows": 1085
      },
      {
        "display_name": "North West Agriculture and Forestry University",
        "institution_id": 4210088176,
        "raw_bridge_rows": 876
      },
      {
        "display_name": "The University of Texas Health Science Center",
        "institution_id": 4210159031,
        "raw_bridge_rows": 696
      },
      {
        "display_name": "Institut Agro Montpelier",
        "institution_id": 4210136436,
        "raw_bridge_rows": 436
      },
      {
        "display_name": "University of Campania \"Luigi Vanvitelli\"",
        "institution_id": 4210126337,
        "raw_bridge_rows": 433
      },
      {
        "display_name": "University of Clermont Auvergne",
        "institution_id": 4210103002,
        "raw_bridge_rows": 430
      },
      {
        "display_name": "Seattle Children's Hospital",
        "institution_id": 4210109034,
        "raw_bridge_rows": 372
      },
      {
        "display_name": "Toulouse Mathematics Institute",
        "institution_id": 4210098964,
        "raw_bridge_rows": 227
      },
      {
        "display_name": "Lurie Children's Hospital",
        "institution_id": 4210125713,
        "raw_bridge_rows": 227
      },
      {
        "display_name": "Autonomous University of Yucat\u00e1n",
        "institution_id": 4210122862,
        "raw_bridge_rows": 181
      },
      {
        "display_name": "ZHAW Zurich University of Applied Sciences",
        "institution_id": 200744771,
        "raw_bridge_rows": 177
      },
      {
        "display_name": "University of Management and Technology",
        "institution_id": 4210089805,
        "raw_bridge_rows": 170
      },
      {
        "display_name": "Beibu Gulf University",
        "institution_id": 4210128032,
        "raw_bridge_rows": 169
      },
      {
        "display_name": "Department of Biomedicine Basel",
        "institution_id": 4210128905,
        "raw_bridge_rows": 166
      },
      {
        "display_name": "Pontificial Catholic University of Valparaiso",
        "institution_id": 4210116133,
        "raw_bridge_rows": 154
      },
      {
        "display_name": "Parul University",
        "institution_id": 4210112983,
        "raw_bridge_rows": 147
      },
      {
        "display_name": "Universit\u00e9 Paul-Val\u00e9ry Montpellier",
        "institution_id": 4210095130,
        "raw_bridge_rows": 139
      },
      {
        "display_name": "Netherlands Cancer Institute-Antoni van Leeuwenhoek Hospital",
        "institution_id": 4210124352,
        "raw_bridge_rows": 138
      },
      {
        "display_name": "The Nature Conservancy",
        "institution_id": 4210093580,
        "raw_bridge_rows": 137
      },
      {
        "display_name": "Federal University of S\u00e3o Jo\u00e3o del-Rei",
        "institution_id": 4210130985,
        "raw_bridge_rows": 134
      },
      {
        "display_name": "Texas A&M Health Science Center",
        "institution_id": 4210105967,
        "raw_bridge_rows": 127
      },
      {
        "display_name": "Klinik und Poliklinik f\u00fcr Hautkrankheiten",
        "institution_id": 4210096309,
        "raw_bridge_rows": 116
      },
      {
        "display_name": "Cracow University of Technology",
        "institution_id": 4210092770,
        "raw_bridge_rows": 113
      }
    ],
    "normalized_sha256": "531e11864e9400d1380f705917458d6c4347a7486fd169b53cdcfed2e0712b5b",
    "queries": [
      {
        "name": "raw_work_rows",
        "result_row_count": 1,
        "result_sha256": "56aabad587204e1a393c30baf149217c0ee158c3b8434f32e4eba7ae0aae34cf",
        "sql": "SELECT count() AS rows, uniqExact(id) AS unique_ids FROM file('tiers/stage2_medium/works/*.parquet', Parquet)",
        "sql_sha256": "5cca43f5303f6f77de8548e48e3b253f4fdd371536eb45f61817dd76a8e3c016"
      },
      {
        "name": "raw_bridge_counts",
        "result_row_count": 1,
        "result_sha256": "10478b44e6fea1feb3051bf9b4625e98038cf06496f8c0fac7d9dc751b5d6494",
        "sql": "SELECT (SELECT count() FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS a WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(a.author.id) IS NOT NULL) AS authors, (SELECT uniqExact(tuple(openalex_numeric_id(id), openalex_numeric_id(a.author.id), openalex_numeric_id(i.id))) FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS a ARRAY JOIN a.institutions AS i WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(a.author.id) IS NOT NULL AND openalex_numeric_id(i.id) IS NOT NULL) AS institutions, (SELECT count() FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN topics AS t WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(t.id) IS NOT NULL AND t.score IS NOT NULL) AS topics",
        "sql_sha256": "93dcf68e68aadb14440aac0c84d26eb71fb4ef267f3bcdd6e390cc1f9703407f"
      },
      {
        "name": "materialized_counts",
        "result_row_count": 1,
        "result_sha256": "047939a06cf113e6883e8e3ade97f07d1b24f1fa5295d68a611feba1140d5de0",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.works) AS works, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_author) AS authors, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_institution) AS institutions, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_topic) AS topics, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.citation_edge) AS citations",
        "sql_sha256": "9779c9752a821fc37897fa60949f5b0098c2a545bf023e701f3a8636dac6fd6c"
      },
      {
        "name": "referential_coverage",
        "result_row_count": 1,
        "result_sha256": "9bfc14c04fcf4b2beb8ad257b9bc2d24f9e5b9f486bac539bfa8a33728e53a50",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.works w ON wa.work_id=w.work_id) AS missing_works_for_authors, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_author) AS author_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.authors a ON wa.author_id=a.author_id) AS missing_authors, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.authors a ON wa.author_id=a.author_id) AS distinct_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.authors a ON wa.author_id=a.author_id) AS works_with_missing_authors, if(author_bridge_rows = 0, 1., 1 - missing_authors / author_bridge_rows) AS author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_author WHERE author_id=9999999999) AS null_author_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_author WHERE author_id=5317838346) AS deleted_author_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_author WHERE author_id NOT IN (9999999999,5317838346)) AS ordinary_authorship_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS ordinary_missing_author_rows, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS distinct_ordinary_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS works_with_ordinary_missing_authors, if(ordinary_authorship_rows = 0, 1., 1 - ordinary_missing_author_rows / ordinary_authorship_rows) AS ordinary_author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_institution) AS institution_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.institutions i ON wi.institution_id=i.institution_id) AS missing_institutions, (SELECT uniqExact(wi.institution_id) FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.institutions i ON wi.institution_id=i.institution_id) AS distinct_missing_institution_ids, (SELECT uniqExact(wi.work_id) FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.institutions i ON wi.institution_id=i.institution_id) AS works_with_missing_institutions, (SELECT uniqExact(wi.author_id) FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.institutions i ON wi.institution_id=i.institution_id) AS authors_with_missing_institutions, if(institution_bridge_rows = 0, 1., (institution_bridge_rows - missing_institutions) / institution_bridge_rows) AS institution_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_topic) AS topic_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.topics t ON wt.topic_id=t.topic_id) AS missing_topics, (SELECT uniqExact(wt.topic_id) FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.topics t ON wt.topic_id=t.topic_id) AS distinct_missing_topic_ids, if(topic_bridge_rows = 0, 1., (topic_bridge_rows - missing_topics) / topic_bridge_rows) AS topic_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.citation_edge) AS citation_edges, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.citation_edge ce INNER JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.works w ON ce.cited_work_id=w.work_id) AS retained_cited_edges, if(citation_edges = 0, 1., retained_cited_edges / citation_edges) AS citation_retention_ratio",
        "sql_sha256": "b6a99084221e238886e626b185029e0275f646a6f0f7c81abbd00f5000cd5379"
      },
      {
        "name": "missing_author_sample",
        "result_row_count": 25,
        "result_sha256": "2029b08cef3cc2b317e2e92a98c1c91cfbed1f75ef27fafca4b6a895f7c9fc95",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wa.author_id FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.authors a ON wa.author_id=a.author_id) SELECT openalex_numeric_id(authorship.author.id) AS author_id, multiIf(author_id=9999999999, 'null_author', author_id=5317838346, 'deleted_author', 'ordinary') AS classification, arraySlice(arraySort(groupUniqArray(ifNull(authorship.author.display_name, ''))), 1, 5) AS display_names, count() AS raw_bridge_rows FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship WHERE openalex_numeric_id(authorship.author.id) IN missing_ids GROUP BY author_id ORDER BY raw_bridge_rows DESC, author_id LIMIT 25",
        "sql_sha256": "f82f09d3959720ed691214d96687f9ed1bfe1f621d00116328035e3e573b53da"
      },
      {
        "name": "missing_institution_sample",
        "result_row_count": 25,
        "result_sha256": "041d556c79b9cc31f860bd11a2eb21e1f96d47e8e9ce9c80b50b2f84fd9f03c5",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wi.institution_id FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.institutions i ON wi.institution_id=i.institution_id) SELECT openalex_numeric_id(raw_institution.id) AS institution_id, any(raw_institution.display_name) AS display_name, count() AS raw_bridge_rows FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship ARRAY JOIN authorship.institutions AS raw_institution WHERE openalex_numeric_id(raw_institution.id) IN missing_ids GROUP BY institution_id ORDER BY raw_bridge_rows DESC, institution_id LIMIT 25",
        "sql_sha256": "5c483ea2015f4dc5fdec80dae039bb19ee61dcecb2293d9994cc35e79b517ce3"
      },
      {
        "name": "works_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "56aabad587204e1a393c30baf149217c0ee158c3b8434f32e4eba7ae0aae34cf",
        "sql": "SELECT count() AS rows, uniqExact(work_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.works",
        "sql_sha256": "b89b042b103d9497499685158adf4fea5684eb9b4264e556923fd07252da55e3"
      },
      {
        "name": "authors_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "ad147b0c2afdbf81139c75c21696b85568b9bd6db2c30818e5fe0d962e8a0170",
        "sql": "SELECT count() AS rows, uniqExact(author_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.authors",
        "sql_sha256": "b706ce1147b66cb0c529020ba11bbe8d4d03f08323c738225156a6539277db85"
      },
      {
        "name": "institutions_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "1d729a2ea001d72722af893931308d2a7ffb55562e2a5a3c33945a1cc15f9c47",
        "sql": "SELECT count() AS rows, uniqExact(institution_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.institutions",
        "sql_sha256": "ca5d9098e60afc7b3291d659810117bda59d566c752f06761ab6c9c902a4540d"
      },
      {
        "name": "sources_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "8515fa4a030ad72ca441f50ae103ac1b7701fb65366d5de9dab09a297ce71e9f",
        "sql": "SELECT count() AS rows, uniqExact(source_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.sources",
        "sql_sha256": "b5271536b9664414396f6a724a6d9a8f34b0676dbd50a0854e3af6f640e214ac"
      },
      {
        "name": "topics_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "83708a811c93190b16a1b7dbe7033261c7a31e9cc7d70ade69ae253c50e5ac75",
        "sql": "SELECT count() AS rows, uniqExact(topic_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.topics",
        "sql_sha256": "ac31e3916b51d7c4d468d9907308d8e983568b7b05d2e6df4ab2f0757e140cf3"
      },
      {
        "name": "year_type_topic_xpac_distribution",
        "result_row_count": 1307378,
        "result_sha256": "9fd1a41a5f5bc8119582c700239d950531afec5124792c9998806df498e7da42",
        "sql": "SELECT publication_year, work_type, primary_topic_id, is_xpac, count() AS works FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.works GROUP BY ALL ORDER BY ALL",
        "sql_sha256": "2d7d357fb35e4c20f024fc67adec8ed7025e160d59b58f5de6d0f61ae99caca3"
      },
      {
        "name": "authorships_per_work",
        "result_row_count": 447,
        "result_sha256": "2bc843d8da3f9998d26c7d558b7c8464e08af5a43f8e0128f60d3aa4c3f77d9e",
        "sql": "SELECT authorships, count() AS works FROM (SELECT work_id, count() AS authorships FROM openalex_stage2_stage2_repeat_medium_18c_36ddc6f2.work_author GROUP BY work_id) GROUP BY authorships ORDER BY authorships",
        "sql_sha256": "57be60e351d423873c62ac441f1eb085f3e9c33dd7d5f36aca02064992413043"
      }
    ],
    "raw_evidence": {
      "distinct_valid_pairs": 70415984,
      "duplicate_pair_delta": 0,
      "null_topic_scores": 0,
      "raw_reference_entries": 70415984,
      "rejected_id_entries": 0
    },
    "referential_coverage": {
      "author_bridge_rows": 16075482,
      "author_reference_coverage_ratio": 0.9979251633014798,
      "authors_with_missing_institutions": 12233,
      "citation_edges": 70415984,
      "citation_retention_ratio": 0.021169738961540324,
      "deleted_author_rows": 0,
      "distinct_missing_author_ids": 238,
      "distinct_missing_institution_ids": 134,
      "distinct_missing_topic_ids": 0,
      "distinct_ordinary_missing_author_ids": 237,
      "institution_bridge_rows": 12517247,
      "institution_reference_coverage_ratio": 0.9988334495596356,
      "missing_authors": 33354,
      "missing_institutions": 14602,
      "missing_topics": 0,
      "missing_works_for_authors": 0,
      "null_author_rows": 33089,
      "ordinary_author_reference_coverage_ratio": 0.9999834812674144,
      "ordinary_authorship_rows": 16042393,
      "ordinary_missing_author_rows": 265,
      "retained_cited_edges": 1490688,
      "topic_bridge_rows": 21657004,
      "topic_reference_coverage_ratio": 1,
      "works_with_missing_authors": 33242,
      "works_with_missing_institutions": 6908,
      "works_with_ordinary_missing_authors": 198
    },
    "sql_sha256": {
      "05_raw_evidence.sql": "486472a3a3a3ec5a2b11d965c4933a6bce4c1bd35dbdb31fe2d694f1c8d40e5a",
      "20_load_works.sql": "c139806aee59508383590b850f2e4178200d02e0cd30c177684d41236effdd5f"
    }
  }
}
```

## Sequential and concurrent evidence

```json
{
  "concurrent": {
    "stage2_medium": {
      "classes": {
        "join": {
          "count": 150,
          "insufficient_sample": false,
          "maximum_seconds": 11.132,
          "median_seconds": 2.998,
          "p95_seconds": 10.881,
          "peak_memory_bytes": 4571436365,
          "read_bytes": 227563532400,
          "read_rows": 10624296150,
          "spill_bytes": 0
        },
        "one_hop": {
          "count": 50,
          "insufficient_sample": false,
          "maximum_seconds": 0.082,
          "median_seconds": 0.006,
          "p95_seconds": 0.011,
          "peak_memory_bytes": 2171974,
          "read_bytes": 574721072,
          "read_rows": 71235184,
          "spill_bytes": 0
        },
        "routine": {
          "count": 99,
          "insufficient_sample": false,
          "maximum_seconds": 1.899,
          "median_seconds": 0.045,
          "p95_seconds": 1.716,
          "peak_memory_bytes": 6777925541,
          "read_bytes": 40987135276,
          "read_rows": 3955869866,
          "spill_bytes": 0
        }
      },
      "execution": {
        "cpus": 18,
        "maximum_seconds": 18000,
        "query_threads": 18,
        "workers": 1
      },
      "first_error": null,
      "forced_verdict": null,
      "merge_activity": {
        "completed_benchmark_merge_count": 0,
        "completed_foreign_merge_count": 0,
        "completed_merge_count": 1844,
        "completed_system_merge_count": 1844,
        "foreign_databases": [],
        "in_flight_benchmark_merge_count": 0,
        "in_flight_foreign_merge_count": 0,
        "in_flight_merge_count": 0,
        "in_flight_system_merge_count": 0,
        "maximum_completed_merge_ms": 1080,
        "maximum_completed_system_merge_ms": 1080,
        "part_log_coverage": {
          "maximum_event_at_unix_us": 1785985224406464,
          "minimum_event_at_unix_us": 1785868945280710,
          "row_count": 51723
        },
        "schema_version": 1,
        "status": "complete"
      },
      "queries": {
        "q01": {
          "count": 50,
          "maximum_seconds": 0.045,
          "median_seconds": 0.027,
          "p95_seconds": 0.037,
          "peak_memory_bytes": 122525559,
          "spill_bytes": 0
        },
        "q02": {
          "count": 50,
          "maximum_seconds": 11.132,
          "median_seconds": 10.54,
          "p95_seconds": 10.949,
          "peak_memory_bytes": 3110317355,
          "spill_bytes": 0
        },
        "q03": {
          "count": 50,
          "maximum_seconds": 3.227,
          "median_seconds": 2.995,
          "p95_seconds": 3.132,
          "peak_memory_bytes": 4571436365,
          "spill_bytes": 0
        },
        "q04": {
          "count": 50,
          "maximum_seconds": 3.131,
          "median_seconds": 2.819,
          "p95_seconds": 2.975,
          "peak_memory_bytes": 2278320148,
          "spill_bytes": 0
        },
        "q05": {
          "count": 50,
          "maximum_seconds": 0.082,
          "median_seconds": 0.006,
          "p95_seconds": 0.011,
          "peak_memory_bytes": 2171974,
          "spill_bytes": 0
        },
        "q07": {
          "count": 49,
          "maximum_seconds": 1.899,
          "median_seconds": 1.595,
          "p95_seconds": 1.737,
          "peak_memory_bytes": 6777925541,
          "spill_bytes": 0
        }
      },
      "server_restarted": false,
      "verdict_cap": "pass"
    }
  },
  "sequential": {
    "stage2_medium": [
      {
        "disk_read_elapsed_us": 33405,
        "elapsed_seconds": 0.059,
        "file_descriptor_read_bytes": 9974352,
        "finished_at_unix_us": 1785984035265753,
        "gating": true,
        "os_cpu_virtual_time_us": 251868,
        "os_cpu_wait_time_us": 20207,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 9974352,
        "page_cache_miss_elapsed_us": 33172,
        "peak_memory_bytes": 122090104,
        "query_class": "routine",
        "query_id": "df512afc-6dbe-5945-a5d1-e55bf577bf44",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 1232559,
        "result_rows": 9810,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984035206941,
        "synchronous_read_wait_us": 144527,
        "system_time_us": 25102,
        "user_time_us": 227026
      },
      {
        "disk_read_elapsed_us": 27133,
        "elapsed_seconds": 0.027,
        "file_descriptor_read_bytes": 10001797,
        "finished_at_unix_us": 1785984035644168,
        "gating": true,
        "os_cpu_virtual_time_us": 230093,
        "os_cpu_wait_time_us": 23576,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10001797,
        "page_cache_miss_elapsed_us": 26928,
        "peak_memory_bytes": 120542483,
        "query_class": "routine",
        "query_id": "daf2a53e-c750-5e2f-860b-e1505cfea366",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 539052,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984035617000,
        "synchronous_read_wait_us": 109124,
        "system_time_us": 13966,
        "user_time_us": 216312
      },
      {
        "disk_read_elapsed_us": 29352,
        "elapsed_seconds": 0.026,
        "file_descriptor_read_bytes": 9877385,
        "finished_at_unix_us": 1785984036020850,
        "gating": true,
        "os_cpu_virtual_time_us": 240052,
        "os_cpu_wait_time_us": 17158,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 9877385,
        "page_cache_miss_elapsed_us": 29100,
        "peak_memory_bytes": 120967185,
        "query_class": "routine",
        "query_id": "d3bb4593-4c92-5135-a170-ffa8c6570ed0",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 526271,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984035994564,
        "synchronous_read_wait_us": 76723,
        "system_time_us": 11489,
        "user_time_us": 228842
      },
      {
        "disk_read_elapsed_us": 29423,
        "elapsed_seconds": 0.025,
        "file_descriptor_read_bytes": 10239997,
        "finished_at_unix_us": 1785984036389251,
        "gating": true,
        "os_cpu_virtual_time_us": 238439,
        "os_cpu_wait_time_us": 25610,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10239997,
        "page_cache_miss_elapsed_us": 29232,
        "peak_memory_bytes": 120964209,
        "query_class": "routine",
        "query_id": "5a32df48-5741-5587-ac89-9ce3aba1a9ab",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 513055,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984036363558,
        "synchronous_read_wait_us": 75950,
        "system_time_us": 17052,
        "user_time_us": 221566
      },
      {
        "disk_read_elapsed_us": 30351,
        "elapsed_seconds": 0.026,
        "file_descriptor_read_bytes": 10025563,
        "finished_at_unix_us": 1785984036761997,
        "gating": true,
        "os_cpu_virtual_time_us": 232294,
        "os_cpu_wait_time_us": 14528,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10025563,
        "page_cache_miss_elapsed_us": 30157,
        "peak_memory_bytes": 121267456,
        "query_class": "routine",
        "query_id": "e04f25c3-0733-5e23-9720-f93eefba728d",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 505073,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984036736204,
        "synchronous_read_wait_us": 74676,
        "system_time_us": 16191,
        "user_time_us": 216280
      },
      {
        "disk_read_elapsed_us": 27107,
        "elapsed_seconds": 0.028,
        "file_descriptor_read_bytes": 10025676,
        "finished_at_unix_us": 1785984037137482,
        "gating": true,
        "os_cpu_virtual_time_us": 245617,
        "os_cpu_wait_time_us": 22329,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10025676,
        "page_cache_miss_elapsed_us": 26880,
        "peak_memory_bytes": 117149555,
        "query_class": "routine",
        "query_id": "3f5f661e-7b16-5e6b-8061-a243b02826cf",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 563819,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984037108859,
        "synchronous_read_wait_us": 71454,
        "system_time_us": 12056,
        "user_time_us": 233740
      },
      {
        "disk_read_elapsed_us": 2504686,
        "elapsed_seconds": 9.586,
        "file_descriptor_read_bytes": 3274152803,
        "finished_at_unix_us": 1785984056767193,
        "gating": true,
        "os_cpu_virtual_time_us": 15693660,
        "os_cpu_wait_time_us": 3263740,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 190164984,
        "page_cache_miss_elapsed_us": 134184,
        "peak_memory_bytes": 3021884588,
        "query_class": "join",
        "query_id": "13595f55-8ce6-5f96-9afd-a4a8889d126a",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 190655806,
        "result_rows": 579800,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984047244793,
        "synchronous_read_wait_us": 381230,
        "system_time_us": 1193833,
        "user_time_us": 14500900
      },
      {
        "disk_read_elapsed_us": 2432614,
        "elapsed_seconds": 9.895,
        "file_descriptor_read_bytes": 3269289178,
        "finished_at_unix_us": 1785984067025892,
        "gating": true,
        "os_cpu_virtual_time_us": 15903718,
        "os_cpu_wait_time_us": 2997365,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 190272870,
        "page_cache_miss_elapsed_us": 128335,
        "peak_memory_bytes": 3083790865,
        "query_class": "join",
        "query_id": "a2848046-3ec2-5022-963e-ecd8f76e25e6",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 196389280,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984057212681,
        "synchronous_read_wait_us": 257462,
        "system_time_us": 1192126,
        "user_time_us": 14712594
      },
      {
        "disk_read_elapsed_us": 2293938,
        "elapsed_seconds": 9.95,
        "file_descriptor_read_bytes": 3134753124,
        "finished_at_unix_us": 1785984077354455,
        "gating": true,
        "os_cpu_virtual_time_us": 16062222,
        "os_cpu_wait_time_us": 3141712,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 190019489,
        "page_cache_miss_elapsed_us": 105980,
        "peak_memory_bytes": 3044079433,
        "query_class": "join",
        "query_id": "5504b261-1dca-5b3c-a586-47a9e9403c20",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 197768749,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984067472025,
        "synchronous_read_wait_us": 240310,
        "system_time_us": 1464848,
        "user_time_us": 14598395
      },
      {
        "disk_read_elapsed_us": 2561725,
        "elapsed_seconds": 10.468,
        "file_descriptor_read_bytes": 3302520262,
        "finished_at_unix_us": 1785984088191263,
        "gating": true,
        "os_cpu_virtual_time_us": 16447736,
        "os_cpu_wait_time_us": 3469106,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 190164036,
        "page_cache_miss_elapsed_us": 120880,
        "peak_memory_bytes": 3076894178,
        "query_class": "join",
        "query_id": "edd03e6a-5f6b-5a3c-9c5b-bc50f3eddaad",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 208128786,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984077785947,
        "synchronous_read_wait_us": 241565,
        "system_time_us": 1621346,
        "user_time_us": 14827405
      },
      {
        "disk_read_elapsed_us": 2482652,
        "elapsed_seconds": 9.844,
        "file_descriptor_read_bytes": 3247497072,
        "finished_at_unix_us": 1785984098421073,
        "gating": true,
        "os_cpu_virtual_time_us": 16409154,
        "os_cpu_wait_time_us": 3073932,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 190010877,
        "page_cache_miss_elapsed_us": 103776,
        "peak_memory_bytes": 3073171505,
        "query_class": "join",
        "query_id": "bfad4687-cb42-5ffe-bbec-e399dc66ffac",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 195721062,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984088640658,
        "synchronous_read_wait_us": 228427,
        "system_time_us": 1448452,
        "user_time_us": 14961749
      },
      {
        "disk_read_elapsed_us": 2929237,
        "elapsed_seconds": 10.395,
        "file_descriptor_read_bytes": 3739378683,
        "finished_at_unix_us": 1785984109170100,
        "gating": true,
        "os_cpu_virtual_time_us": 16787168,
        "os_cpu_wait_time_us": 3770943,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 190011082,
        "page_cache_miss_elapsed_us": 110659,
        "peak_memory_bytes": 3076117763,
        "query_class": "join",
        "query_id": "c63b7a6c-1bb7-5a2d-8f4b-edc4eb13fe71",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 206365018,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984098858900,
        "synchronous_read_wait_us": 227732,
        "system_time_us": 1573198,
        "user_time_us": 15214973
      },
      {
        "disk_read_elapsed_us": 3101293,
        "elapsed_seconds": 2.729,
        "file_descriptor_read_bytes": 3042272490,
        "finished_at_unix_us": 1785984122087932,
        "gating": true,
        "os_cpu_virtual_time_us": 14101282,
        "os_cpu_wait_time_us": 1365830,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2734349954,
        "page_cache_miss_elapsed_us": 2770851,
        "peak_memory_bytes": 4369060689,
        "query_class": "join",
        "query_id": "55a2bf14-7bc6-50bb-b8f8-e7afc7b5a6d8",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 57266095,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984119372963,
        "synchronous_read_wait_us": 5899935,
        "system_time_us": 1344792,
        "user_time_us": 12766820
      },
      {
        "disk_read_elapsed_us": 3308020,
        "elapsed_seconds": 2.826,
        "file_descriptor_read_bytes": 3044577423,
        "finished_at_unix_us": 1785984125309569,
        "gating": true,
        "os_cpu_virtual_time_us": 14398521,
        "os_cpu_wait_time_us": 1340979,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2736653070,
        "page_cache_miss_elapsed_us": 3006743,
        "peak_memory_bytes": 4402530443,
        "query_class": "join",
        "query_id": "68b45e30-86bb-5487-9691-09331c63a648",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 59311773,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984122499633,
        "synchronous_read_wait_us": 6374907,
        "system_time_us": 1361737,
        "user_time_us": 13046290
      },
      {
        "disk_read_elapsed_us": 3296781,
        "elapsed_seconds": 2.686,
        "file_descriptor_read_bytes": 3045232932,
        "finished_at_unix_us": 1785984128383700,
        "gating": true,
        "os_cpu_virtual_time_us": 14602097,
        "os_cpu_wait_time_us": 1308978,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2737228998,
        "page_cache_miss_elapsed_us": 2958914,
        "peak_memory_bytes": 4360237900,
        "query_class": "join",
        "query_id": "c3ea97aa-7c10-5851-805d-648e39c76f4d",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 56509056,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984125714037,
        "synchronous_read_wait_us": 6069307,
        "system_time_us": 1441414,
        "user_time_us": 13170288
      },
      {
        "disk_read_elapsed_us": 3476963,
        "elapsed_seconds": 2.819,
        "file_descriptor_read_bytes": 3043708036,
        "finished_at_unix_us": 1785984131567571,
        "gating": true,
        "os_cpu_virtual_time_us": 14650246,
        "os_cpu_wait_time_us": 1287595,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2735720014,
        "page_cache_miss_elapsed_us": 3125491,
        "peak_memory_bytes": 4375474831,
        "query_class": "join",
        "query_id": "02ca305d-ad37-5cb1-a79a-a037ed6dc1df",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 59240292,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984128763910,
        "synchronous_read_wait_us": 6396564,
        "system_time_us": 1478012,
        "user_time_us": 13182131
      },
      {
        "disk_read_elapsed_us": 3591331,
        "elapsed_seconds": 2.775,
        "file_descriptor_read_bytes": 3046326894,
        "finished_at_unix_us": 1785984134719638,
        "gating": true,
        "os_cpu_virtual_time_us": 14848881,
        "os_cpu_wait_time_us": 1254554,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2738341454,
        "page_cache_miss_elapsed_us": 3247519,
        "peak_memory_bytes": 4362792745,
        "query_class": "join",
        "query_id": "5e44ed1a-1a6c-53c4-963f-15b1773e443c",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 58590285,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984131960508,
        "synchronous_read_wait_us": 6571633,
        "system_time_us": 1505885,
        "user_time_us": 13352959
      },
      {
        "disk_read_elapsed_us": 3238985,
        "elapsed_seconds": 2.909,
        "file_descriptor_read_bytes": 3044616352,
        "finished_at_unix_us": 1785984137993977,
        "gating": true,
        "os_cpu_virtual_time_us": 15005674,
        "os_cpu_wait_time_us": 1459380,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2736665009,
        "page_cache_miss_elapsed_us": 2920057,
        "peak_memory_bytes": 4383977110,
        "query_class": "join",
        "query_id": "940ad897-60ba-5c49-9760-e4c1df1d7253",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 60916859,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984135101571,
        "synchronous_read_wait_us": 6165911,
        "system_time_us": 1575141,
        "user_time_us": 13439248
      },
      {
        "disk_read_elapsed_us": 156544,
        "elapsed_seconds": 2.493,
        "file_descriptor_read_bytes": 136715542,
        "finished_at_unix_us": 1785984150997961,
        "gating": true,
        "os_cpu_virtual_time_us": 5124446,
        "os_cpu_wait_time_us": 23240,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 136715542,
        "page_cache_miss_elapsed_us": 155512,
        "peak_memory_bytes": 2269766243,
        "query_class": "join",
        "query_id": "7ba2143e-1129-5b61-aa62-5815d203c396",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 49982609,
        "result_rows": 110456,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984148505442,
        "synchronous_read_wait_us": 315857,
        "system_time_us": 88640,
        "user_time_us": 5036655
      },
      {
        "disk_read_elapsed_us": 102466,
        "elapsed_seconds": 2.481,
        "file_descriptor_read_bytes": 136691110,
        "finished_at_unix_us": 1785984153835170,
        "gating": true,
        "os_cpu_virtual_time_us": 5147970,
        "os_cpu_wait_time_us": 16989,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 136691110,
        "page_cache_miss_elapsed_us": 101548,
        "peak_memory_bytes": 2263582617,
        "query_class": "join",
        "query_id": "cedb075c-63d5-5b0e-95b3-395ba6ca4d9a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 49606016,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984151354206,
        "synchronous_read_wait_us": 197403,
        "system_time_us": 73306,
        "user_time_us": 5075360
      },
      {
        "disk_read_elapsed_us": 125158,
        "elapsed_seconds": 2.542,
        "file_descriptor_read_bytes": 137050629,
        "finished_at_unix_us": 1785984156716117,
        "gating": true,
        "os_cpu_virtual_time_us": 5165069,
        "os_cpu_wait_time_us": 15418,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137050629,
        "page_cache_miss_elapsed_us": 124190,
        "peak_memory_bytes": 2259772743,
        "query_class": "join",
        "query_id": "9801aa14-b9e6-5fd2-b51f-036a8ddf9c9a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 50875248,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984154175088,
        "synchronous_read_wait_us": 222057,
        "system_time_us": 79685,
        "user_time_us": 5086227
      },
      {
        "disk_read_elapsed_us": 97672,
        "elapsed_seconds": 2.566,
        "file_descriptor_read_bytes": 136832438,
        "finished_at_unix_us": 1785984159669954,
        "gating": true,
        "os_cpu_virtual_time_us": 5217747,
        "os_cpu_wait_time_us": 19263,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 136832438,
        "page_cache_miss_elapsed_us": 96715,
        "peak_memory_bytes": 2259480123,
        "query_class": "join",
        "query_id": "cac9576c-5bbd-5797-b028-2d781cf4f7c1",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 51332474,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984157104043,
        "synchronous_read_wait_us": 197437,
        "system_time_us": 91923,
        "user_time_us": 5126665
      },
      {
        "disk_read_elapsed_us": 113698,
        "elapsed_seconds": 2.547,
        "file_descriptor_read_bytes": 136811034,
        "finished_at_unix_us": 1785984162555931,
        "gating": true,
        "os_cpu_virtual_time_us": 5195902,
        "os_cpu_wait_time_us": 20139,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 136811034,
        "page_cache_miss_elapsed_us": 112807,
        "peak_memory_bytes": 2263182225,
        "query_class": "join",
        "query_id": "0810c65e-2c98-5cd1-b43c-bfb4c95a789a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 50970317,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984160009289,
        "synchronous_read_wait_us": 210922,
        "system_time_us": 104049,
        "user_time_us": 5092602
      },
      {
        "disk_read_elapsed_us": 109846,
        "elapsed_seconds": 2.544,
        "file_descriptor_read_bytes": 137081297,
        "finished_at_unix_us": 1785984165460488,
        "gating": true,
        "os_cpu_virtual_time_us": 5173168,
        "os_cpu_wait_time_us": 15256,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137081297,
        "page_cache_miss_elapsed_us": 108853,
        "peak_memory_bytes": 2260592832,
        "query_class": "join",
        "query_id": "3b30e5aa-2e1a-5868-8c48-f7db737325cd",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 50923539,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984162916865,
        "synchronous_read_wait_us": 211237,
        "system_time_us": 91209,
        "user_time_us": 5082633
      },
      {
        "disk_read_elapsed_us": 625979,
        "elapsed_seconds": 0.087,
        "file_descriptor_read_bytes": 415775265,
        "finished_at_unix_us": 1785984175674136,
        "gating": true,
        "os_cpu_virtual_time_us": 478331,
        "os_cpu_wait_time_us": 60061,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 415701492,
        "page_cache_miss_elapsed_us": 624554,
        "peak_memory_bytes": 2181968,
        "query_class": "one_hop",
        "query_id": "b730b9c4-9614-57b4-b429-efae8d8cca95",
        "query_name": "q05",
        "read_bytes": 563458944,
        "read_rows": 70432368,
        "real_time_us": 2549228,
        "result_rows": 0,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984175587061,
        "synchronous_read_wait_us": 1198159,
        "system_time_us": 188185,
        "user_time_us": 291753
      },
      {
        "disk_read_elapsed_us": 788092,
        "elapsed_seconds": 0.089,
        "file_descriptor_read_bytes": 414119877,
        "finished_at_unix_us": 1785984176125571,
        "gating": true,
        "os_cpu_virtual_time_us": 502887,
        "os_cpu_wait_time_us": 66600,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 414119877,
        "page_cache_miss_elapsed_us": 786642,
        "peak_memory_bytes": 2178830,
        "query_class": "one_hop",
        "query_id": "4c447197-0298-5dcc-863c-bb68268e94b7",
        "query_name": "q05",
        "read_bytes": 563555736,
        "read_rows": 70432368,
        "real_time_us": 2545163,
        "result_rows": 46,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984176035834,
        "synchronous_read_wait_us": 1166139,
        "system_time_us": 197448,
        "user_time_us": 307093
      },
      {
        "disk_read_elapsed_us": 835708,
        "elapsed_seconds": 0.092,
        "file_descriptor_read_bytes": 413674006,
        "finished_at_unix_us": 1785984176600307,
        "gating": true,
        "os_cpu_virtual_time_us": 522362,
        "os_cpu_wait_time_us": 93485,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 413674006,
        "page_cache_miss_elapsed_us": 833997,
        "peak_memory_bytes": 2248646,
        "query_class": "one_hop",
        "query_id": "cecc163f-7a64-5b1a-8a6b-67432d383cf3",
        "query_name": "q05",
        "read_bytes": 563590016,
        "read_rows": 70432368,
        "real_time_us": 2657803,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984176507629,
        "synchronous_read_wait_us": 1220020,
        "system_time_us": 199990,
        "user_time_us": 323370
      },
      {
        "disk_read_elapsed_us": 0,
        "elapsed_seconds": 0.001,
        "file_descriptor_read_bytes": 0,
        "finished_at_unix_us": 1785984176941958,
        "gating": true,
        "os_cpu_virtual_time_us": 1052,
        "os_cpu_wait_time_us": 0,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 0,
        "page_cache_miss_elapsed_us": 0,
        "peak_memory_bytes": 317488,
        "query_class": "one_hop",
        "query_id": "56847c14-8888-5648-b76e-e6bcc1efb0fe",
        "query_name": "q05",
        "read_bytes": 0,
        "read_rows": 0,
        "real_time_us": 1347,
        "result_rows": 0,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984176940838,
        "synchronous_read_wait_us": 0,
        "system_time_us": 17,
        "user_time_us": 1036
      },
      {
        "disk_read_elapsed_us": 227,
        "elapsed_seconds": 0.006,
        "file_descriptor_read_bytes": 105193,
        "finished_at_unix_us": 1785984177280304,
        "gating": true,
        "os_cpu_virtual_time_us": 11001,
        "os_cpu_wait_time_us": 18,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 105193,
        "page_cache_miss_elapsed_us": 222,
        "peak_memory_bytes": 355542,
        "query_class": "one_hop",
        "query_id": "05433fc9-a0fd-5105-a0bf-222b56ccdaee",
        "query_name": "q05",
        "read_bytes": 227864,
        "read_rows": 16384,
        "real_time_us": 29623,
        "result_rows": 46,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984177273449,
        "synchronous_read_wait_us": 465,
        "system_time_us": 9058,
        "user_time_us": 1946
      },
      {
        "disk_read_elapsed_us": 249,
        "elapsed_seconds": 0.002,
        "file_descriptor_read_bytes": 83533,
        "finished_at_unix_us": 1785984177609089,
        "gating": true,
        "os_cpu_virtual_time_us": 2073,
        "os_cpu_wait_time_us": 21,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 83533,
        "page_cache_miss_elapsed_us": 247,
        "peak_memory_bytes": 435830,
        "query_class": "one_hop",
        "query_id": "4d1ec754-13eb-50d6-a22c-98ed007e69a9",
        "query_name": "q05",
        "read_bytes": 262144,
        "read_rows": 16384,
        "real_time_us": 6132,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984177606925,
        "synchronous_read_wait_us": 479,
        "system_time_us": 1093,
        "user_time_us": 988
      },
      {
        "disk_read_elapsed_us": 547,
        "elapsed_seconds": 0.004,
        "file_descriptor_read_bytes": 101562,
        "finished_at_unix_us": 1785984186689638,
        "gating": false,
        "os_cpu_virtual_time_us": 4974,
        "os_cpu_wait_time_us": 451,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 27789,
        "page_cache_miss_elapsed_us": 195,
        "peak_memory_bytes": 502912,
        "query_class": "two_hop",
        "query_id": "e3fe4ac0-fa86-5a02-8efd-25c540966369",
        "query_name": "q06",
        "read_bytes": 131072,
        "read_rows": 16384,
        "real_time_us": 26427,
        "result_rows": 1,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984186685458,
        "synchronous_read_wait_us": 566,
        "system_time_us": 3181,
        "user_time_us": 1812
      },
      {
        "disk_read_elapsed_us": 881303,
        "elapsed_seconds": 0.1,
        "file_descriptor_read_bytes": 452538769,
        "finished_at_unix_us": 1785984187181430,
        "gating": false,
        "os_cpu_virtual_time_us": 674080,
        "os_cpu_wait_time_us": 119275,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 452538769,
        "page_cache_miss_elapsed_us": 879351,
        "peak_memory_bytes": 4922074,
        "query_class": "two_hop",
        "query_id": "9d2e2953-22dd-5b31-b4e5-9cf8066454f2",
        "query_name": "q06",
        "read_bytes": 1126883608,
        "read_rows": 70432368,
        "real_time_us": 2879536,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984187080922,
        "synchronous_read_wait_us": 1277563,
        "system_time_us": 191236,
        "user_time_us": 484426
      },
      {
        "disk_read_elapsed_us": 708931,
        "elapsed_seconds": 0.097,
        "file_descriptor_read_bytes": 452517748,
        "finished_at_unix_us": 1785984187627190,
        "gating": false,
        "os_cpu_virtual_time_us": 692429,
        "os_cpu_wait_time_us": 103241,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 452517748,
        "page_cache_miss_elapsed_us": 707137,
        "peak_memory_bytes": 13293901,
        "query_class": "two_hop",
        "query_id": "31906d93-f6aa-506e-9e0d-98386489f28e",
        "query_name": "q06",
        "read_bytes": 1126917888,
        "read_rows": 70432368,
        "real_time_us": 2600414,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984187530236,
        "synchronous_read_wait_us": 1105603,
        "system_time_us": 186427,
        "user_time_us": 507736
      },
      {
        "disk_read_elapsed_us": 89,
        "elapsed_seconds": 0.003,
        "file_descriptor_read_bytes": 8840,
        "finished_at_unix_us": 1785984187976984,
        "gating": false,
        "os_cpu_virtual_time_us": 4812,
        "os_cpu_wait_time_us": 2,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 8840,
        "page_cache_miss_elapsed_us": 87,
        "peak_memory_bytes": 494712,
        "query_class": "two_hop",
        "query_id": "8be06a02-9757-5ba0-b974-acaa423bac3f",
        "query_name": "q06",
        "read_bytes": 131072,
        "read_rows": 16384,
        "real_time_us": 27600,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984187973601,
        "synchronous_read_wait_us": 205,
        "system_time_us": 1937,
        "user_time_us": 2890
      },
      {
        "disk_read_elapsed_us": 810235,
        "elapsed_seconds": 0.099,
        "file_descriptor_read_bytes": 453179408,
        "finished_at_unix_us": 1785984188425157,
        "gating": false,
        "os_cpu_virtual_time_us": 675351,
        "os_cpu_wait_time_us": 85923,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 453179408,
        "page_cache_miss_elapsed_us": 808263,
        "peak_memory_bytes": 5243083,
        "query_class": "two_hop",
        "query_id": "ca252312-d31a-51f9-97b5-8e8957b9d0f9",
        "query_name": "q06",
        "read_bytes": 1126883608,
        "read_rows": 70432368,
        "real_time_us": 2760622,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984188326229,
        "synchronous_read_wait_us": 1195451,
        "system_time_us": 210195,
        "user_time_us": 466760
      },
      {
        "disk_read_elapsed_us": 811773,
        "elapsed_seconds": 0.101,
        "file_descriptor_read_bytes": 452710244,
        "finished_at_unix_us": 1785984188842326,
        "gating": false,
        "os_cpu_virtual_time_us": 710173,
        "os_cpu_wait_time_us": 88487,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 452710244,
        "page_cache_miss_elapsed_us": 809624,
        "peak_memory_bytes": 15381672,
        "query_class": "two_hop",
        "query_id": "06e16dca-0cb0-5a21-a590-9ab54e9aecf3",
        "query_name": "q06",
        "read_bytes": 1126917888,
        "read_rows": 70432368,
        "real_time_us": 2831862,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984188740864,
        "synchronous_read_wait_us": 1183558,
        "system_time_us": 181318,
        "user_time_us": 530128
      },
      {
        "disk_read_elapsed_us": 786936,
        "elapsed_seconds": 1.234,
        "file_descriptor_read_bytes": 902261431,
        "finished_at_unix_us": 1785984200023349,
        "gating": true,
        "os_cpu_virtual_time_us": 17207034,
        "os_cpu_wait_time_us": 1071295,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426892781,
        "page_cache_miss_elapsed_us": 258944,
        "peak_memory_bytes": 6405896521,
        "query_class": "routine",
        "query_id": "98beb1b8-f4dc-5c3f-8698-b25017f646c8",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24690397,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984198809528,
        "synchronous_read_wait_us": 1346493,
        "system_time_us": 601676,
        "user_time_us": 16607365
      },
      {
        "disk_read_elapsed_us": 786732,
        "elapsed_seconds": 1.215,
        "file_descriptor_read_bytes": 901809024,
        "finished_at_unix_us": 1785984201631712,
        "gating": true,
        "os_cpu_virtual_time_us": 17091642,
        "os_cpu_wait_time_us": 1026318,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426960645,
        "page_cache_miss_elapsed_us": 245370,
        "peak_memory_bytes": 6181845495,
        "query_class": "routine",
        "query_id": "8f02c1e1-b7c5-5c70-90de-d5aac44f331b",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24135534,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984200436860,
        "synchronous_read_wait_us": 919817,
        "system_time_us": 545588,
        "user_time_us": 16548149
      },
      {
        "disk_read_elapsed_us": 851750,
        "elapsed_seconds": 1.237,
        "file_descriptor_read_bytes": 902141188,
        "finished_at_unix_us": 1785984203228273,
        "gating": true,
        "os_cpu_virtual_time_us": 17126505,
        "os_cpu_wait_time_us": 1434834,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426737350,
        "page_cache_miss_elapsed_us": 263171,
        "peak_memory_bytes": 6097885933,
        "query_class": "routine",
        "query_id": "58755398-ae4b-5258-8d79-71348767369e",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24641663,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984202011020,
        "synchronous_read_wait_us": 1305484,
        "system_time_us": 604713,
        "user_time_us": 16524011
      },
      {
        "disk_read_elapsed_us": 874213,
        "elapsed_seconds": 1.25,
        "file_descriptor_read_bytes": 901232443,
        "finished_at_unix_us": 1785984204841584,
        "gating": true,
        "os_cpu_virtual_time_us": 17350532,
        "os_cpu_wait_time_us": 1049806,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426712961,
        "page_cache_miss_elapsed_us": 285742,
        "peak_memory_bytes": 6014292693,
        "query_class": "routine",
        "query_id": "ca0b271f-58da-5e7a-ae72-b5fb29797641",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24906495,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984203611706,
        "synchronous_read_wait_us": 1118720,
        "system_time_us": 602398,
        "user_time_us": 16750076
      },
      {
        "disk_read_elapsed_us": 944991,
        "elapsed_seconds": 1.261,
        "file_descriptor_read_bytes": 902449161,
        "finished_at_unix_us": 1785984206448714,
        "gating": true,
        "os_cpu_virtual_time_us": 17539888,
        "os_cpu_wait_time_us": 1299561,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426729246,
        "page_cache_miss_elapsed_us": 293124,
        "peak_memory_bytes": 5891569125,
        "query_class": "routine",
        "query_id": "590f6f1c-a94f-543d-9cc9-292c8eca5018",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 25079620,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984205210885,
        "synchronous_read_wait_us": 1151196,
        "system_time_us": 574028,
        "user_time_us": 16967543
      },
      {
        "disk_read_elapsed_us": 838950,
        "elapsed_seconds": 1.257,
        "file_descriptor_read_bytes": 901272756,
        "finished_at_unix_us": 1785984208072425,
        "gating": true,
        "os_cpu_virtual_time_us": 17559676,
        "os_cpu_wait_time_us": 1167675,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426691814,
        "page_cache_miss_elapsed_us": 246153,
        "peak_memory_bytes": 6381819901,
        "query_class": "routine",
        "query_id": "37eecc92-ac52-54ae-8794-7f5398c6662d",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 25034355,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785984206834072,
        "synchronous_read_wait_us": 1209960,
        "system_time_us": 652071,
        "user_time_us": 16910215
      }
    ]
  }
}
```

## Storage and capacity evidence

```json
{
  "capacity_model_status": "not yet validated at full corpus scale",
  "dimension_samples": [
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 65127188
      },
      "timestamp": 1785983969.378252
    },
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 353812270
      },
      "timestamp": 1785983970.597707
    },
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 604334732
      },
      "timestamp": 1785983971.798629
    },
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 874789034
      },
      "timestamp": 1785983973.007346
    },
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1156630868
      },
      "timestamp": 1785983974.228746
    },
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1403408102
      },
      "timestamp": 1785983975.475264
    },
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1467785874
      },
      "timestamp": 1785983976.709975
    },
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1656866012
      },
      "timestamp": 1785983977.948947
    },
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1809726903
      },
      "timestamp": 1785983979.176976
    },
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2056133761
      },
      "timestamp": 1785983980.414874
    },
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2297823085
      },
      "timestamp": 1785983981.6379972
    },
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2542250650
      },
      "timestamp": 1785983982.850348
    },
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2792598403
      },
      "timestamp": 1785983984.092937
    },
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3015152949
      },
      "timestamp": 1785983985.306735
    },
    {
      "filesystem_bytes": 3420209152,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3296679959
      },
      "timestamp": 1785983986.5229702
    },
    {
      "filesystem_bytes": 11199000576,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3400278950,
        "institutions": 4357308,
        "sources": 10677280,
        "topics": 150309
      },
      "timestamp": 1785983987.4942222
    }
  ],
  "tiers": {
    "stage2_medium": [
      {
        "filesystem_bytes": 12292038656,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3371248772,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 22755270
        },
        "timestamp": 1785983992.9810948
      },
      {
        "filesystem_bytes": 12292038656,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3371248772,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 220363033
        },
        "timestamp": 1785983994.298086
      },
      {
        "filesystem_bytes": 12292038656,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3371248772,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 220363033
        },
        "timestamp": 1785983995.5362408
      },
      {
        "filesystem_bytes": 12292038656,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348693099,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213472308
        },
        "timestamp": 1785983996.773258
      },
      {
        "filesystem_bytes": 12292038656,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348693099,
          "citation_edge": 100331855,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213472308
        },
        "timestamp": 1785983998.0069811
      },
      {
        "filesystem_bytes": 12292038656,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348693099,
          "citation_edge": 241011376,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213472308
        },
        "timestamp": 1785983999.220822
      },
      {
        "filesystem_bytes": 12292038656,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348693099,
          "citation_edge": 368400708,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213472308
        },
        "timestamp": 1785984000.4289799
      },
      {
        "filesystem_bytes": 12292038656,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348693099,
          "citation_edge": 520249407,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213472308
        },
        "timestamp": 1785984001.641217
      },
      {
        "filesystem_bytes": 12292038656,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348693099,
          "citation_edge": 580800844,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 32315904,
          "works": 213472308
        },
        "timestamp": 1785984002.8986712
      },
      {
        "filesystem_bytes": 12292038656,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348693099,
          "citation_edge": 580800844,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 139618716,
          "works": 213472308
        },
        "timestamp": 1785984004.136344
      },
      {
        "filesystem_bytes": 12292038656,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348693099,
          "citation_edge": 516259932,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159182598,
          "work_institution": 8990230,
          "works": 213472308
        },
        "timestamp": 1785984005.371764
      },
      {
        "filesystem_bytes": 12292038656,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348693099,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159182598,
          "work_institution": 54565725,
          "works": 213472308
        },
        "timestamp": 1785984006.604243
      },
      {
        "filesystem_bytes": 12292038656,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348693099,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159182598,
          "work_institution": 78732726,
          "works": 213472308
        },
        "timestamp": 1785984007.818686
      },
      {
        "filesystem_bytes": 12292038656,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348693099,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159182598,
          "work_institution": 100950688,
          "work_topic": 71478793,
          "works": 213472308
        },
        "timestamp": 1785984009.044557
      },
      {
        "filesystem_bytes": 15694245888,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348693099,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159182598,
          "work_institution": 100950688,
          "work_topic": 202565014,
          "works": 213472308
        },
        "timestamp": 1785984010.597653
      }
    ]
  }
}
```

Scaling slopes are empirical evidence from sampled tiers; they are not a full-size prediction.

## Limitations

- This local Stage 2 run executed the requested 50 GiB ClickHouse container with 18 CPUs, 1 concurrent worker(s), and 18 query threads; no resource fallback was attempted.
- The OpenAlex manifests publish byte lengths and record counts but no content checksum; verification checks size and Parquet footer row counts and does not claim cryptographic object integrity.
- The Works samples are stratified by updated_date and are not a population-representative sample.
- Local Apple Silicon and local SSD latency is not extrapolated to an Alliance x86 VM with network-backed storage.
- The Alliance performance envelope remains unvalidated.
- stage2_medium: the canonical Authors snapshot leaves 33354 of 16075482 Work-author bridge rows unresolved, including 33089 documented NULL-author rows and 0 documented deleted-author rows. The ordinary unresolved count is 265 of 16042393 (coverage 0.9999834813; blocking floor 0.999000). Raw links are preserved; use LEFT JOIN when unmatched authorships matter.
