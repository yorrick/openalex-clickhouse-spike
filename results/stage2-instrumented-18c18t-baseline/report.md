# OpenAlex ClickHouse validation — stage2-instrumented-18c18t-baseline

Local engine verdict: conditional

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
        "00_schema.sql": "5c67d0be9611696c5b7e175955e1fef45199a22ade3260e0f8f9da8ff8f5b359",
        "11_load_complete_authors.sql": "4868a887ee7a334614adb271a94c4abc531863c988aad8516025259a5a70ee4d",
        "12_load_small_dimensions.sql": "1957a5a9be504c8035de9408fafb1ee397d8970a47b87b84d782afd81ba4c1b2",
        "30_reverse_projection.sql": "1d429578b85160eed289de6a895116ffa04f9001a589f7db5f615a21eeec6665",
        "stage2_large/05_raw_evidence.sql": "093f45e5f4da6e10fdc41cd301d1c2822866d11da167f74d1c753c8e1e84bbf5",
        "stage2_large/20_load_works.sql": "d02aa846faa7b4d3ec5ccf0369bd3f981dd92b0795e42180d41eb3045c20ec18",
        "stage2_medium/05_raw_evidence.sql": "486472a3a3a3ec5a2b11d965c4933a6bce4c1bd35dbdb31fe2d694f1c8d40e5a",
        "stage2_medium/20_load_works.sql": "d21d03fdb067d1ebc0b50724b451b44a7b0d785132eceed2641ec12935de94d6",
        "stage2_small/05_raw_evidence.sql": "797a7ccfaecba47b213e1664e925a39e284aeed47a89b71106934db9f0950681",
        "stage2_small/20_load_works.sql": "731fcec7e55121827dee7f1806feffe213c322d67754b14a4dd1c4ea7f674144"
      },
      "run_id": "stage2-instrumented-18c18t-baseline",
      "selection_sha256": "ccc7b5c51f04bd5972e6fb513f15157c13a79300be5fc5c36696aebbf56026b1",
      "sha256": "e429481bee51ca50f37a64fbf796e230f477d47dc4aa0d179e74c88072505125",
      "tiers": [
        "stage2_small",
        "stage2_medium",
        "stage2_large"
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
      "stage2_large": {
        "content_length": 45233146344,
        "record_count": 31885241
      },
      "stage2_medium": {
        "content_length": 15118229383,
        "record_count": 10109733
      },
      "stage2_small": {
        "content_length": 3254297980,
        "record_count": 2002982
      }
    }
  }
}
```

## Correctness

```json
{
  "stage2_large": {
    "distribution_digests": {
      "authorships_per_work": {
        "item_count": 843,
        "sha256": "6265ea4756058c8ed86bfe5c3b998dec58901617cbb497a620400b6f1d78d37a",
        "value_kind": "rows"
      },
      "materialized_counts": {
        "item_count": 5,
        "sha256": "9f3a6cab3fb965d44b09d32dfdcbee73f70c7493ac2194cdb374b2cd64b5cd89",
        "value_kind": "object"
      },
      "missing_author_sample": {
        "item_count": 25,
        "sha256": "44359b4810798de7ec48cf6afb714bab06c06352e3a0b1b9d5ddd4284d670dbe",
        "value_kind": "rows"
      },
      "missing_institution_sample": {
        "item_count": 25,
        "sha256": "0a5d7a24775cc990e0818eb12f1d49eedfbd8ffa2d44d159193ecceb3427c05a",
        "value_kind": "rows"
      },
      "referential_coverage": {
        "item_count": 26,
        "sha256": "c9704085735bf9827654717ee6668badceec146058e22167abcfbe0817838dd1",
        "value_kind": "object"
      },
      "year_type_topic_xpac": {
        "item_count": 2201659,
        "sha256": "687cd62516f49aa16089bac525ce076838eeb289cadba49f0bf4c99b9192028f",
        "value_kind": "rows"
      }
    },
    "gates": [
      {
        "actual": 31885241,
        "blocking": true,
        "evidence": {
          "query": "raw_work_rows"
        },
        "expected": 31885241,
        "name": "manifest_rows_match_parquet",
        "passed": true
      },
      {
        "actual": 31885241,
        "blocking": true,
        "evidence": {
          "query": "raw_work_rows"
        },
        "expected": 31885241,
        "name": "raw_work_ids_are_unique",
        "passed": true
      },
      {
        "actual": 0,
        "blocking": true,
        "evidence": {
          "raw_evidence": {
            "distinct_valid_pairs": 208787187,
            "duplicate_pair_delta": 0,
            "null_topic_scores": 0,
            "raw_reference_entries": 208787187,
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
            "distinct_valid_pairs": 208787187,
            "duplicate_pair_delta": 0,
            "null_topic_scores": 0,
            "raw_reference_entries": 208787187,
            "rejected_id_entries": 0
          }
        },
        "expected": 0,
        "name": "topic_scores_are_non_null",
        "passed": true
      },
      {
        "actual": 51816498,
        "blocking": true,
        "evidence": {
          "raw_query": "raw_bridge_counts",
          "table_query": "materialized_counts"
        },
        "expected": 51816498,
        "name": "authors_bridge_reconciles",
        "passed": true
      },
      {
        "actual": 39499697,
        "blocking": true,
        "evidence": {
          "raw_query": "raw_bridge_counts",
          "table_query": "materialized_counts"
        },
        "expected": 39499697,
        "name": "institutions_bridge_reconciles",
        "passed": true
      },
      {
        "actual": 64589578,
        "blocking": true,
        "evidence": {
          "raw_query": "raw_bridge_counts",
          "table_query": "materialized_counts"
        },
        "expected": 64589578,
        "name": "topics_bridge_reconciles",
        "passed": true
      },
      {
        "actual": 208787187,
        "blocking": true,
        "evidence": {
          "duplicate_pair_delta": 0
        },
        "expected": 208787187,
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
        "actual": 98331,
        "blocking": false,
        "evidence": {
          "affected_works": 96601,
          "deleted_author_rows": 0,
          "distinct_missing_ids": 4267,
          "null_author_rows": 93593,
          "overall_coverage": 0.9981023225459968,
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
        "actual": 0.9999083964831442,
        "blocking": true,
        "evidence": {
          "affected_works": 3197,
          "distinct_ordinary_missing_ids": 4266,
          "excluded_special_author_ids": [
            9999999999,
            5317838346
          ],
          "ordinary_authorship_rows": 51722905,
          "ordinary_missing_rows": 4738,
          "query": "referential_coverage",
          "zero_denominator_convention": "coverage is 1 only when ordinary_authorship_rows is zero; authors_bridge_reconciles independently pins total bridge rows"
        },
        "expected": ">=0.999000",
        "name": "ordinary_author_reference_coverage",
        "passed": true
      },
      {
        "actual": 45252,
        "blocking": false,
        "evidence": {
          "distinct_missing_ids": 143,
          "query": "referential_coverage",
          "sample_query": "missing_institution_sample"
        },
        "expected": 0,
        "name": "missing_institutions",
        "passed": false
      },
      {
        "actual": 31885241,
        "blocking": true,
        "evidence": {
          "query": "works_id_uniqueness"
        },
        "expected": 31885241,
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
          "!D.o.w.n.l.o.a.d e-Book A New Earth: Awakening to Your Life's Purpose (Oprah's Book Club, Selection 61) Pre Order",
          "!D.o.w.n.l.o.a.d e-Book Alberto Vargas: Works from the Max Vargas Collection Full PDF",
          "!D.o.w.n.l.o.a.d e-Book Conjoint Behavioral Consultation: Promoting Family-School Connections and Interventions Full PDF",
          "!D.o.w.n.l.o.a.d e-Book Egyptian Hieroglyphs for Complete Beginners [Full]"
        ],
        "raw_bridge_rows": 93593
      },
      {
        "author_id": 5013217494,
        "classification": "ordinary",
        "display_names": [
          "F Xavier Medina",
          "F. X. Medina",
          "F. Xavier Medina",
          "Francesc-Xavier Medina"
        ],
        "raw_bridge_rows": 19
      },
      {
        "author_id": 5101601286,
        "classification": "ordinary",
        "display_names": [
          "ADYE, T",
          "Adye, T.",
          "Adye, Tim",
          "FRANEK, B",
          "Franek, B."
        ],
        "raw_bridge_rows": 10
      },
      {
        "author_id": 5103165407,
        "classification": "ordinary",
        "display_names": [
          "Baden, A",
          "Cline, D",
          "Conway, R",
          "Erhan, S",
          "Grothe, M"
        ],
        "raw_bridge_rows": 10
      },
      {
        "author_id": 5108107655,
        "classification": "ordinary",
        "display_names": [
          "Jos\u00e8 Angel Brandariz Garcia",
          "Jos\u00e9 A Brandariz",
          "Jos\u00e9 A. Brandariz",
          "Jos\u00e9 Brandariz",
          "Jos\u00e9 \u00c1ngel Brandariz"
        ],
        "raw_bridge_rows": 10
      },
      {
        "author_id": 5016264137,
        "classification": "ordinary",
        "display_names": [
          "Allison, J.",
          "Allison,J  E",
          "D'Orazio, A.",
          "Ferrarotto, F.",
          "Smith, A. J. S."
        ],
        "raw_bridge_rows": 9
      },
      {
        "author_id": 5051855142,
        "classification": "ordinary",
        "display_names": [
          "Alexey Svyatkovskiy",
          "Boulahouache, C",
          "Calpas, B",
          "Garfinkel, Arthur F",
          "Guragain, S"
        ],
        "raw_bridge_rows": 9
      },
      {
        "author_id": 5063807156,
        "classification": "ordinary",
        "display_names": [
          "D. Redolar-Ripoll",
          "Diego Redolar",
          "Diego Redolar Ripoll",
          "Diego Redolar-Ripoll"
        ],
        "raw_bridge_rows": 9
      },
      {
        "author_id": 5015883457,
        "classification": "ordinary",
        "display_names": [
          "Porter, SR"
        ],
        "raw_bridge_rows": 8
      },
      {
        "author_id": 5042802063,
        "classification": "ordinary",
        "display_names": [
          "Blount, N. L.",
          "Dujmic, D.",
          "Kroeger, R",
          "Kroeger, R.",
          "Roberts, D. A."
        ],
        "raw_bridge_rows": 8
      },
      {
        "author_id": 5015228672,
        "classification": "ordinary",
        "display_names": [
          "Kerth, L. T.",
          "Kerth, L.T.",
          "Piatenko, T.",
          "Porter, F. C.",
          "Porter, F.C."
        ],
        "raw_bridge_rows": 7
      },
      {
        "author_id": 5100768677,
        "classification": "ordinary",
        "display_names": [
          "Alverson, G",
          "Anastassov, A",
          "Anastassov, Anton Iankov",
          "Snow, GR",
          "Won, S"
        ],
        "raw_bridge_rows": 7
      },
      {
        "author_id": 5100772144,
        "classification": "ordinary",
        "display_names": [
          "Berry, E",
          "Christopher, G",
          "Ferapontov, A",
          "Garabedian, A",
          "Lazic, D"
        ],
        "raw_bridge_rows": 7
      },
      {
        "author_id": 5101601348,
        "classification": "ordinary",
        "display_names": [
          "A. Martelli",
          "Martelli, A."
        ],
        "raw_bridge_rows": 7
      },
      {
        "author_id": 5028565447,
        "classification": "ordinary",
        "display_names": [
          "Coleman, J. P.",
          "Convery, M. R.",
          "Convery, M.R.",
          "Mandelkern, M.",
          "Ofte, I."
        ],
        "raw_bridge_rows": 6
      },
      {
        "author_id": 5046727604,
        "classification": "ordinary",
        "display_names": [
          "Drummond, B. W.",
          "Eckmann, R.",
          "Izen, J. M.",
          "Izen, J.M.",
          "Izen, Joseph Michael"
        ],
        "raw_bridge_rows": 6
      },
      {
        "author_id": 5055923147,
        "classification": "ordinary",
        "display_names": [
          "Coulomb, Jean-Louis",
          "Labie, Patrice"
        ],
        "raw_bridge_rows": 6
      },
      {
        "author_id": 5089425828,
        "classification": "ordinary",
        "display_names": [
          "Barlow, R. J.",
          "Bloom, P.",
          "Bloom, P. C.",
          "Gabathuler, E.",
          "Hutchcroft, D. E."
        ],
        "raw_bridge_rows": 6
      },
      {
        "author_id": 5100732691,
        "classification": "ordinary",
        "display_names": [
          "BOSIO, C",
          "Longo, E",
          "Micheli, F",
          "Sigamani, M",
          "Sigamani, M."
        ],
        "raw_bridge_rows": 6
      },
      {
        "author_id": 5101850539,
        "classification": "ordinary",
        "display_names": [
          "Lange, J",
          "Lellouch, J",
          "Lellouch, J.",
          "Naumann-Emme, S",
          "Nowak, F"
        ],
        "raw_bridge_rows": 6
      },
      {
        "author_id": 5001448296,
        "classification": "ordinary",
        "display_names": [
          "Bochenek, J",
          "Furic, IK",
          "Haas, J",
          "Hagopian, S"
        ],
        "raw_bridge_rows": 5
      },
      {
        "author_id": 5007666223,
        "classification": "ordinary",
        "display_names": [
          "Fanfani, A",
          "Fasanella, D",
          "Giunta, M",
          "Grandi, C",
          "P. Giacomelli"
        ],
        "raw_bridge_rows": 5
      },
      {
        "author_id": 5010638529,
        "classification": "ordinary",
        "display_names": [
          "Kadastik, M",
          "Kamel, AE",
          "M. A. Mahmoud",
          "Mahmoud, MA",
          "Radi, A"
        ],
        "raw_bridge_rows": 5
      },
      {
        "author_id": 5013700119,
        "classification": "ordinary",
        "display_names": [
          "Adye, T.",
          "De Groot, N.",
          "TIMMERMANS, J",
          "Waldi, R."
        ],
        "raw_bridge_rows": 5
      },
      {
        "author_id": 5014187615,
        "classification": "ordinary",
        "display_names": [
          "Morton, G.W.",
          "Nash, J.A.",
          "Pulliam, T.",
          "Rahimi, A. M.",
          "Raymond, DM"
        ],
        "raw_bridge_rows": 5
      }
    ],
    "missing_institution_sample": [
      {
        "display_name": "Tampere University",
        "institution_id": 4210133110,
        "raw_bridge_rows": 9637
      },
      {
        "display_name": "Southwestern Medical Center",
        "institution_id": 4210096815,
        "raw_bridge_rows": 6285
      },
      {
        "display_name": "National Yang Ming Chiao Tung University",
        "institution_id": 96323854,
        "raw_bridge_rows": 3397
      },
      {
        "display_name": "North West Agriculture and Forestry University",
        "institution_id": 4210088176,
        "raw_bridge_rows": 2487
      },
      {
        "display_name": "The University of Texas Health Science Center",
        "institution_id": 4210159031,
        "raw_bridge_rows": 2058
      },
      {
        "display_name": "Institut Agro Montpelier",
        "institution_id": 4210136436,
        "raw_bridge_rows": 1524
      },
      {
        "display_name": "University of Clermont Auvergne",
        "institution_id": 4210103002,
        "raw_bridge_rows": 1366
      },
      {
        "display_name": "University of Campania \"Luigi Vanvitelli\"",
        "institution_id": 4210126337,
        "raw_bridge_rows": 1285
      },
      {
        "display_name": "Seattle Children's Hospital",
        "institution_id": 4210109034,
        "raw_bridge_rows": 1118
      },
      {
        "display_name": "Lurie Children's Hospital",
        "institution_id": 4210125713,
        "raw_bridge_rows": 706
      },
      {
        "display_name": "ZHAW Zurich University of Applied Sciences",
        "institution_id": 200744771,
        "raw_bridge_rows": 637
      },
      {
        "display_name": "Toulouse Mathematics Institute",
        "institution_id": 4210098964,
        "raw_bridge_rows": 619
      },
      {
        "display_name": "Universit\u00e9 Paul-Val\u00e9ry Montpellier",
        "institution_id": 4210095130,
        "raw_bridge_rows": 579
      },
      {
        "display_name": "Klinik und Poliklinik f\u00fcr Hautkrankheiten",
        "institution_id": 4210096309,
        "raw_bridge_rows": 577
      },
      {
        "display_name": "Department of Biomedicine Basel",
        "institution_id": 4210128905,
        "raw_bridge_rows": 539
      },
      {
        "display_name": "Autonomous University of Yucat\u00e1n",
        "institution_id": 4210122862,
        "raw_bridge_rows": 501
      },
      {
        "display_name": "Universit\u00e4tsklinik f\u00fcr Neurologie",
        "institution_id": 4210090358,
        "raw_bridge_rows": 489
      },
      {
        "display_name": "Beibu Gulf University",
        "institution_id": 4210128032,
        "raw_bridge_rows": 467
      },
      {
        "display_name": "Parul University",
        "institution_id": 4210112983,
        "raw_bridge_rows": 456
      },
      {
        "display_name": "Netherlands Cancer Institute-Antoni van Leeuwenhoek Hospital",
        "institution_id": 4210124352,
        "raw_bridge_rows": 443
      },
      {
        "display_name": "University of Management and Technology",
        "institution_id": 4210089805,
        "raw_bridge_rows": 440
      },
      {
        "display_name": "Pontificial Catholic University of Valparaiso",
        "institution_id": 4210116133,
        "raw_bridge_rows": 436
      },
      {
        "display_name": "Texas A&M Health Science Center",
        "institution_id": 4210105967,
        "raw_bridge_rows": 423
      },
      {
        "display_name": "Universit\u00e4tsklinik f\u00fcr Hals-, Nasen- und Ohrenkrankheiten",
        "institution_id": 4210087698,
        "raw_bridge_rows": 406
      },
      {
        "display_name": "Chinese Journal of Integrated Traditional and Western Medicine",
        "institution_id": 4210147667,
        "raw_bridge_rows": 391
      }
    ],
    "normalized_sha256": "55d9f93cd6fb278e926c729ef145f832f6fccde8619b109b864d65fbe4a9271e",
    "queries": [
      {
        "name": "raw_work_rows",
        "result_row_count": 1,
        "result_sha256": "eec0816fb4eaeb19b8e4f555e3bcc79a63a63336b547593e4c25222d510d205e",
        "sql": "SELECT count() AS rows, uniqExact(id) AS unique_ids FROM file('tiers/stage2_large/works/*.parquet', Parquet)",
        "sql_sha256": "017f1dd0a5fd7f07d4b544540ed968e21c14114c57a7cf13d2c50209589c3bdb"
      },
      {
        "name": "raw_bridge_counts",
        "result_row_count": 1,
        "result_sha256": "b0207da15eefbf11842b7aea30aabf4570521393824ec0a55ee5ed84619c390c",
        "sql": "SELECT (SELECT count() FROM file('tiers/stage2_large/works/*.parquet', Parquet) ARRAY JOIN authorships AS a WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(a.author.id) IS NOT NULL) AS authors, (SELECT uniqExact(tuple(openalex_numeric_id(id), openalex_numeric_id(a.author.id), openalex_numeric_id(i.id))) FROM file('tiers/stage2_large/works/*.parquet', Parquet) ARRAY JOIN authorships AS a ARRAY JOIN a.institutions AS i WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(a.author.id) IS NOT NULL AND openalex_numeric_id(i.id) IS NOT NULL) AS institutions, (SELECT count() FROM file('tiers/stage2_large/works/*.parquet', Parquet) ARRAY JOIN topics AS t WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(t.id) IS NOT NULL AND t.score IS NOT NULL) AS topics",
        "sql_sha256": "d82e79ca08cd3be4f53ba4859e783e1b09a754c3c3c4139691592f05b37d6311"
      },
      {
        "name": "materialized_counts",
        "result_row_count": 1,
        "result_sha256": "f0d975bfc2305eee9d784a27dab52796f806fc6c72f46e6cd887d2b1aa15587c",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.works) AS works, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author) AS authors, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution) AS institutions, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_topic) AS topics, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.citation_edge) AS citations",
        "sql_sha256": "1034bcd28d120a2027a77515894dca5779123edf6979498d4cede4817949581d"
      },
      {
        "name": "referential_coverage",
        "result_row_count": 1,
        "result_sha256": "97a87bcbd1e7199e574988b6c7ebc35e1cb86ab5bc2e171e387b43c4013534fe",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.works w ON wa.work_id=w.work_id) AS missing_works_for_authors, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author) AS author_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id) AS missing_authors, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id) AS distinct_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id) AS works_with_missing_authors, if(author_bridge_rows = 0, 1., 1 - missing_authors / author_bridge_rows) AS author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author WHERE author_id=9999999999) AS null_author_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author WHERE author_id=5317838346) AS deleted_author_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author WHERE author_id NOT IN (9999999999,5317838346)) AS ordinary_authorship_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS ordinary_missing_author_rows, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS distinct_ordinary_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS works_with_ordinary_missing_authors, if(ordinary_authorship_rows = 0, 1., 1 - ordinary_missing_author_rows / ordinary_authorship_rows) AS ordinary_author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution) AS institution_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) AS missing_institutions, (SELECT uniqExact(wi.institution_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) AS distinct_missing_institution_ids, (SELECT uniqExact(wi.work_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) AS works_with_missing_institutions, (SELECT uniqExact(wi.author_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) AS authors_with_missing_institutions, if(institution_bridge_rows = 0, 1., (institution_bridge_rows - missing_institutions) / institution_bridge_rows) AS institution_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_topic) AS topic_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.topics t ON wt.topic_id=t.topic_id) AS missing_topics, (SELECT uniqExact(wt.topic_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.topics t ON wt.topic_id=t.topic_id) AS distinct_missing_topic_ids, if(topic_bridge_rows = 0, 1., (topic_bridge_rows - missing_topics) / topic_bridge_rows) AS topic_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.citation_edge) AS citation_edges, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.citation_edge ce INNER JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.works w ON ce.cited_work_id=w.work_id) AS retained_cited_edges, if(citation_edges = 0, 1., retained_cited_edges / citation_edges) AS citation_retention_ratio",
        "sql_sha256": "1798f1e6655531fb6188577d88d93bdd964bb00992efdcf1a64ad60d1e72f999"
      },
      {
        "name": "missing_author_sample",
        "result_row_count": 25,
        "result_sha256": "44359b4810798de7ec48cf6afb714bab06c06352e3a0b1b9d5ddd4284d670dbe",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wa.author_id FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id) SELECT openalex_numeric_id(authorship.author.id) AS author_id, multiIf(author_id=9999999999, 'null_author', author_id=5317838346, 'deleted_author', 'ordinary') AS classification, arraySlice(arraySort(groupUniqArray(ifNull(authorship.author.display_name, ''))), 1, 5) AS display_names, count() AS raw_bridge_rows FROM file('tiers/stage2_large/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship WHERE openalex_numeric_id(authorship.author.id) IN missing_ids GROUP BY author_id ORDER BY raw_bridge_rows DESC, author_id LIMIT 25",
        "sql_sha256": "1475d5d6dcc08758dfed63b76f55114fcc33e09806bfba62b0c564b075b15b6b"
      },
      {
        "name": "missing_institution_sample",
        "result_row_count": 25,
        "result_sha256": "0a5d7a24775cc990e0818eb12f1d49eedfbd8ffa2d44d159193ecceb3427c05a",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wi.institution_id FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) SELECT openalex_numeric_id(raw_institution.id) AS institution_id, any(raw_institution.display_name) AS display_name, count() AS raw_bridge_rows FROM file('tiers/stage2_large/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship ARRAY JOIN authorship.institutions AS raw_institution WHERE openalex_numeric_id(raw_institution.id) IN missing_ids GROUP BY institution_id ORDER BY raw_bridge_rows DESC, institution_id LIMIT 25",
        "sql_sha256": "19c20959466dc4c13c4bff92ee81f7161d87b2166437b123384d1d6f20b1cce0"
      },
      {
        "name": "works_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "eec0816fb4eaeb19b8e4f555e3bcc79a63a63336b547593e4c25222d510d205e",
        "sql": "SELECT count() AS rows, uniqExact(work_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.works",
        "sql_sha256": "a54c0fb3d18dcd02ed53a840790d7973e1dc8170eea48ea4335d20b35d299679"
      },
      {
        "name": "authors_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "ad147b0c2afdbf81139c75c21696b85568b9bd6db2c30818e5fe0d962e8a0170",
        "sql": "SELECT count() AS rows, uniqExact(author_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.authors",
        "sql_sha256": "200051495727abc3514bed465df41bebe27c063b6fee465fe23ef469dd8dbf85"
      },
      {
        "name": "institutions_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "1d729a2ea001d72722af893931308d2a7ffb55562e2a5a3c33945a1cc15f9c47",
        "sql": "SELECT count() AS rows, uniqExact(institution_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions",
        "sql_sha256": "757a66a097fa2d64b91dc2421042c308344cb73c5357fadbeda04642fdee8c88"
      },
      {
        "name": "sources_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "8515fa4a030ad72ca441f50ae103ac1b7701fb65366d5de9dab09a297ce71e9f",
        "sql": "SELECT count() AS rows, uniqExact(source_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.sources",
        "sql_sha256": "2cffeeefb3c19dc9d29bcc96b418636c52a72ad1211d0129f663c3b0930a14f7"
      },
      {
        "name": "topics_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "83708a811c93190b16a1b7dbe7033261c7a31e9cc7d70ade69ae253c50e5ac75",
        "sql": "SELECT count() AS rows, uniqExact(topic_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.topics",
        "sql_sha256": "ce4bf89d0bfd351946fa215f3e6d8b843c16a9000c3634036880e73fc02472a8"
      },
      {
        "name": "year_type_topic_xpac_distribution",
        "result_row_count": 2201659,
        "result_sha256": "687cd62516f49aa16089bac525ce076838eeb289cadba49f0bf4c99b9192028f",
        "sql": "SELECT publication_year, work_type, primary_topic_id, is_xpac, count() AS works FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.works GROUP BY ALL ORDER BY ALL",
        "sql_sha256": "1ef536038c3b3b49ba3d50fee3df969241d692eae667c87e94fae1acdec18aa6"
      },
      {
        "name": "authorships_per_work",
        "result_row_count": 843,
        "result_sha256": "6265ea4756058c8ed86bfe5c3b998dec58901617cbb497a620400b6f1d78d37a",
        "sql": "SELECT authorships, count() AS works FROM (SELECT work_id, count() AS authorships FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author GROUP BY work_id) GROUP BY authorships ORDER BY authorships",
        "sql_sha256": "8f0630e0c24ae39834589df78b9ec41c24f32100d26af4debaf0ba9e3dd7db22"
      }
    ],
    "raw_evidence": {
      "distinct_valid_pairs": 208787187,
      "duplicate_pair_delta": 0,
      "null_topic_scores": 0,
      "raw_reference_entries": 208787187,
      "rejected_id_entries": 0
    },
    "referential_coverage": {
      "author_bridge_rows": 51816498,
      "author_reference_coverage_ratio": 0.9981023225459968,
      "authors_with_missing_institutions": 32185,
      "citation_edges": 208787187,
      "citation_retention_ratio": 0.06572912924967948,
      "deleted_author_rows": 0,
      "distinct_missing_author_ids": 4267,
      "distinct_missing_institution_ids": 143,
      "distinct_missing_topic_ids": 0,
      "distinct_ordinary_missing_author_ids": 4266,
      "institution_bridge_rows": 39499697,
      "institution_reference_coverage_ratio": 0.9988543709588455,
      "missing_authors": 98331,
      "missing_institutions": 45252,
      "missing_topics": 0,
      "missing_works_for_authors": 0,
      "null_author_rows": 93593,
      "ordinary_author_reference_coverage_ratio": 0.9999083964831442,
      "ordinary_authorship_rows": 51722905,
      "ordinary_missing_author_rows": 4738,
      "retained_cited_edges": 13723400,
      "topic_bridge_rows": 64589578,
      "topic_reference_coverage_ratio": 1,
      "works_with_missing_authors": 96601,
      "works_with_missing_institutions": 21716,
      "works_with_ordinary_missing_authors": 3197
    },
    "sql_sha256": {
      "05_raw_evidence.sql": "093f45e5f4da6e10fdc41cd301d1c2822866d11da167f74d1c753c8e1e84bbf5",
      "20_load_works.sql": "d02aa846faa7b4d3ec5ccf0369bd3f981dd92b0795e42180d41eb3045c20ec18"
    }
  },
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
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.works) AS works, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author) AS authors, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution) AS institutions, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_topic) AS topics, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.citation_edge) AS citations",
        "sql_sha256": "1034bcd28d120a2027a77515894dca5779123edf6979498d4cede4817949581d"
      },
      {
        "name": "referential_coverage",
        "result_row_count": 1,
        "result_sha256": "9bfc14c04fcf4b2beb8ad257b9bc2d24f9e5b9f486bac539bfa8a33728e53a50",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.works w ON wa.work_id=w.work_id) AS missing_works_for_authors, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author) AS author_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id) AS missing_authors, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id) AS distinct_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id) AS works_with_missing_authors, if(author_bridge_rows = 0, 1., 1 - missing_authors / author_bridge_rows) AS author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author WHERE author_id=9999999999) AS null_author_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author WHERE author_id=5317838346) AS deleted_author_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author WHERE author_id NOT IN (9999999999,5317838346)) AS ordinary_authorship_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS ordinary_missing_author_rows, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS distinct_ordinary_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS works_with_ordinary_missing_authors, if(ordinary_authorship_rows = 0, 1., 1 - ordinary_missing_author_rows / ordinary_authorship_rows) AS ordinary_author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution) AS institution_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) AS missing_institutions, (SELECT uniqExact(wi.institution_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) AS distinct_missing_institution_ids, (SELECT uniqExact(wi.work_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) AS works_with_missing_institutions, (SELECT uniqExact(wi.author_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) AS authors_with_missing_institutions, if(institution_bridge_rows = 0, 1., (institution_bridge_rows - missing_institutions) / institution_bridge_rows) AS institution_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_topic) AS topic_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.topics t ON wt.topic_id=t.topic_id) AS missing_topics, (SELECT uniqExact(wt.topic_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.topics t ON wt.topic_id=t.topic_id) AS distinct_missing_topic_ids, if(topic_bridge_rows = 0, 1., (topic_bridge_rows - missing_topics) / topic_bridge_rows) AS topic_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.citation_edge) AS citation_edges, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.citation_edge ce INNER JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.works w ON ce.cited_work_id=w.work_id) AS retained_cited_edges, if(citation_edges = 0, 1., retained_cited_edges / citation_edges) AS citation_retention_ratio",
        "sql_sha256": "1798f1e6655531fb6188577d88d93bdd964bb00992efdcf1a64ad60d1e72f999"
      },
      {
        "name": "missing_author_sample",
        "result_row_count": 25,
        "result_sha256": "2029b08cef3cc2b317e2e92a98c1c91cfbed1f75ef27fafca4b6a895f7c9fc95",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wa.author_id FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id) SELECT openalex_numeric_id(authorship.author.id) AS author_id, multiIf(author_id=9999999999, 'null_author', author_id=5317838346, 'deleted_author', 'ordinary') AS classification, arraySlice(arraySort(groupUniqArray(ifNull(authorship.author.display_name, ''))), 1, 5) AS display_names, count() AS raw_bridge_rows FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship WHERE openalex_numeric_id(authorship.author.id) IN missing_ids GROUP BY author_id ORDER BY raw_bridge_rows DESC, author_id LIMIT 25",
        "sql_sha256": "a00395ca4341f4882a9e26a04b2d341868b13f5ed1b4ac1540efdca22be077ed"
      },
      {
        "name": "missing_institution_sample",
        "result_row_count": 25,
        "result_sha256": "041d556c79b9cc31f860bd11a2eb21e1f96d47e8e9ce9c80b50b2f84fd9f03c5",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wi.institution_id FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) SELECT openalex_numeric_id(raw_institution.id) AS institution_id, any(raw_institution.display_name) AS display_name, count() AS raw_bridge_rows FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship ARRAY JOIN authorship.institutions AS raw_institution WHERE openalex_numeric_id(raw_institution.id) IN missing_ids GROUP BY institution_id ORDER BY raw_bridge_rows DESC, institution_id LIMIT 25",
        "sql_sha256": "a11f0d89679c53bcf0a9fe814fad22bddb2f2b23bf584031e8924f051071bc79"
      },
      {
        "name": "works_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "56aabad587204e1a393c30baf149217c0ee158c3b8434f32e4eba7ae0aae34cf",
        "sql": "SELECT count() AS rows, uniqExact(work_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.works",
        "sql_sha256": "a54c0fb3d18dcd02ed53a840790d7973e1dc8170eea48ea4335d20b35d299679"
      },
      {
        "name": "authors_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "ad147b0c2afdbf81139c75c21696b85568b9bd6db2c30818e5fe0d962e8a0170",
        "sql": "SELECT count() AS rows, uniqExact(author_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.authors",
        "sql_sha256": "200051495727abc3514bed465df41bebe27c063b6fee465fe23ef469dd8dbf85"
      },
      {
        "name": "institutions_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "1d729a2ea001d72722af893931308d2a7ffb55562e2a5a3c33945a1cc15f9c47",
        "sql": "SELECT count() AS rows, uniqExact(institution_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions",
        "sql_sha256": "757a66a097fa2d64b91dc2421042c308344cb73c5357fadbeda04642fdee8c88"
      },
      {
        "name": "sources_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "8515fa4a030ad72ca441f50ae103ac1b7701fb65366d5de9dab09a297ce71e9f",
        "sql": "SELECT count() AS rows, uniqExact(source_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.sources",
        "sql_sha256": "2cffeeefb3c19dc9d29bcc96b418636c52a72ad1211d0129f663c3b0930a14f7"
      },
      {
        "name": "topics_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "83708a811c93190b16a1b7dbe7033261c7a31e9cc7d70ade69ae253c50e5ac75",
        "sql": "SELECT count() AS rows, uniqExact(topic_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.topics",
        "sql_sha256": "ce4bf89d0bfd351946fa215f3e6d8b843c16a9000c3634036880e73fc02472a8"
      },
      {
        "name": "year_type_topic_xpac_distribution",
        "result_row_count": 1307378,
        "result_sha256": "9fd1a41a5f5bc8119582c700239d950531afec5124792c9998806df498e7da42",
        "sql": "SELECT publication_year, work_type, primary_topic_id, is_xpac, count() AS works FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.works GROUP BY ALL ORDER BY ALL",
        "sql_sha256": "1ef536038c3b3b49ba3d50fee3df969241d692eae667c87e94fae1acdec18aa6"
      },
      {
        "name": "authorships_per_work",
        "result_row_count": 447,
        "result_sha256": "2bc843d8da3f9998d26c7d558b7c8464e08af5a43f8e0128f60d3aa4c3f77d9e",
        "sql": "SELECT authorships, count() AS works FROM (SELECT work_id, count() AS authorships FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author GROUP BY work_id) GROUP BY authorships ORDER BY authorships",
        "sql_sha256": "8f0630e0c24ae39834589df78b9ec41c24f32100d26af4debaf0ba9e3dd7db22"
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
      "20_load_works.sql": "d21d03fdb067d1ebc0b50724b451b44a7b0d785132eceed2641ec12935de94d6"
    }
  },
  "stage2_small": {
    "distribution_digests": {
      "authorships_per_work": {
        "item_count": 200,
        "sha256": "8c704127e6d040ac4779ce338b625f61ecd0f9a7faee500ee1f59850b8dc3b38",
        "value_kind": "rows"
      },
      "materialized_counts": {
        "item_count": 5,
        "sha256": "534006b323a9366b702a0c26ae80f3bc899bdfc3650deaf3e399a2dcbf2aceb8",
        "value_kind": "object"
      },
      "missing_author_sample": {
        "item_count": 14,
        "sha256": "99a76bcebd2eb596aad11499de36d0f0433fdd046319d0bec9237a41f9f28082",
        "value_kind": "rows"
      },
      "missing_institution_sample": {
        "item_count": 25,
        "sha256": "e76891d77558501c47c0f69c20680983202e0d65482fb85bfcbd131b4f66f365",
        "value_kind": "rows"
      },
      "referential_coverage": {
        "item_count": 26,
        "sha256": "cb6afcad7dc161d569c5d040c29dd299fa9399bee7898a8122370679f32d73ca",
        "value_kind": "object"
      },
      "year_type_topic_xpac": {
        "item_count": 492399,
        "sha256": "89b42e728db3c8983e10ef0e5324c51deb698afea5daa05dcefcf53b0917024e",
        "value_kind": "rows"
      }
    },
    "gates": [
      {
        "actual": 2002982,
        "blocking": true,
        "evidence": {
          "query": "raw_work_rows"
        },
        "expected": 2002982,
        "name": "manifest_rows_match_parquet",
        "passed": true
      },
      {
        "actual": 2002982,
        "blocking": true,
        "evidence": {
          "query": "raw_work_rows"
        },
        "expected": 2002982,
        "name": "raw_work_ids_are_unique",
        "passed": true
      },
      {
        "actual": 0,
        "blocking": true,
        "evidence": {
          "raw_evidence": {
            "distinct_valid_pairs": 15283016,
            "duplicate_pair_delta": 0,
            "null_topic_scores": 0,
            "raw_reference_entries": 15283016,
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
            "distinct_valid_pairs": 15283016,
            "duplicate_pair_delta": 0,
            "null_topic_scores": 0,
            "raw_reference_entries": 15283016,
            "rejected_id_entries": 0
          }
        },
        "expected": 0,
        "name": "topic_scores_are_non_null",
        "passed": true
      },
      {
        "actual": 3852081,
        "blocking": true,
        "evidence": {
          "raw_query": "raw_bridge_counts",
          "table_query": "materialized_counts"
        },
        "expected": 3852081,
        "name": "authors_bridge_reconciles",
        "passed": true
      },
      {
        "actual": 2646224,
        "blocking": true,
        "evidence": {
          "raw_query": "raw_bridge_counts",
          "table_query": "materialized_counts"
        },
        "expected": 2646224,
        "name": "institutions_bridge_reconciles",
        "passed": true
      },
      {
        "actual": 4139113,
        "blocking": true,
        "evidence": {
          "raw_query": "raw_bridge_counts",
          "table_query": "materialized_counts"
        },
        "expected": 4139113,
        "name": "topics_bridge_reconciles",
        "passed": true
      },
      {
        "actual": 15283016,
        "blocking": true,
        "evidence": {
          "duplicate_pair_delta": 0
        },
        "expected": 15283016,
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
        "actual": 8133,
        "blocking": false,
        "evidence": {
          "affected_works": 8117,
          "deleted_author_rows": 0,
          "distinct_missing_ids": 14,
          "null_author_rows": 8118,
          "overall_coverage": 0.9978886736805379,
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
        "actual": 0.9999960977772159,
        "blocking": true,
        "evidence": {
          "affected_works": 14,
          "distinct_ordinary_missing_ids": 13,
          "excluded_special_author_ids": [
            9999999999,
            5317838346
          ],
          "ordinary_authorship_rows": 3843963,
          "ordinary_missing_rows": 15,
          "query": "referential_coverage",
          "zero_denominator_convention": "coverage is 1 only when ordinary_authorship_rows is zero; authors_bridge_reconciles independently pins total bridge rows"
        },
        "expected": ">=0.999000",
        "name": "ordinary_author_reference_coverage",
        "passed": true
      },
      {
        "actual": 3133,
        "blocking": false,
        "evidence": {
          "distinct_missing_ids": 122,
          "query": "referential_coverage",
          "sample_query": "missing_institution_sample"
        },
        "expected": 0,
        "name": "missing_institutions",
        "passed": false
      },
      {
        "actual": 2002982,
        "blocking": true,
        "evidence": {
          "query": "works_id_uniqueness"
        },
        "expected": 2002982,
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
          "\"\u0413\u04af\u043b\u043d\u0430\u0440\u0430 \u049a\u0430\u043d\u0430\u0442\u049b\u044b\u0437\u044b \u049a\u04b1\u0440\u043c\u0430\u043d\u0493\u0430\u043b\u0438 \"",
          "&NA;",
          "&NA; &NA;",
          ","
        ],
        "raw_bridge_rows": 8118
      },
      {
        "author_id": 5013217494,
        "classification": "ordinary",
        "display_names": [
          "F. Xavier Medina"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5108107655,
        "classification": "ordinary",
        "display_names": [
          "Jos\u00e9 \u00c1ngel Brandariz",
          "Jos\u00e9 \u00c1ngel Brandariz Garc\u00eda"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5005691707,
        "classification": "ordinary",
        "display_names": [
          "Weixin Liang"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5033480771,
        "classification": "ordinary",
        "display_names": [
          "Krstulovic, Giorgio"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5040314307,
        "classification": "ordinary",
        "display_names": [
          "Chunhua Yang"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5076742397,
        "classification": "ordinary",
        "display_names": [
          "Alwyn Cheung"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5090532047,
        "classification": "ordinary",
        "display_names": [
          "Elena Planas"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5100450860,
        "classification": "ordinary",
        "display_names": [
          "Yongsheng Han"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5102966505,
        "classification": "ordinary",
        "display_names": [
          "Mads F. Hansen"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5106093995,
        "classification": "ordinary",
        "display_names": [
          "Adina Dusa"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5111751828,
        "classification": "ordinary",
        "display_names": [
          "Peter Robins"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5118904739,
        "classification": "ordinary",
        "display_names": [
          "Arendt, D."
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5118904740,
        "classification": "ordinary",
        "display_names": [
          "Arndt, Thomas Channing"
        ],
        "raw_bridge_rows": 1
      }
    ],
    "missing_institution_sample": [
      {
        "display_name": "Tampere University",
        "institution_id": 4210133110,
        "raw_bridge_rows": 660
      },
      {
        "display_name": "Southwestern Medical Center",
        "institution_id": 4210096815,
        "raw_bridge_rows": 473
      },
      {
        "display_name": "National Yang Ming Chiao Tung University",
        "institution_id": 96323854,
        "raw_bridge_rows": 150
      },
      {
        "display_name": "North West Agriculture and Forestry University",
        "institution_id": 4210088176,
        "raw_bridge_rows": 149
      },
      {
        "display_name": "University of Campania \"Luigi Vanvitelli\"",
        "institution_id": 4210126337,
        "raw_bridge_rows": 110
      },
      {
        "display_name": "Institut Agro Montpelier",
        "institution_id": 4210136436,
        "raw_bridge_rows": 108
      },
      {
        "display_name": "The University of Texas Health Science Center",
        "institution_id": 4210159031,
        "raw_bridge_rows": 99
      },
      {
        "display_name": "University of Clermont Auvergne",
        "institution_id": 4210103002,
        "raw_bridge_rows": 98
      },
      {
        "display_name": "Seattle Children's Hospital",
        "institution_id": 4210109034,
        "raw_bridge_rows": 75
      },
      {
        "display_name": "Department of Biomedicine Basel",
        "institution_id": 4210128905,
        "raw_bridge_rows": 68
      },
      {
        "display_name": "Autonomous University of Yucat\u00e1n",
        "institution_id": 4210122862,
        "raw_bridge_rows": 60
      },
      {
        "display_name": "Toulouse Mathematics Institute",
        "institution_id": 4210098964,
        "raw_bridge_rows": 58
      },
      {
        "display_name": "University of Management and Technology",
        "institution_id": 4210089805,
        "raw_bridge_rows": 54
      },
      {
        "display_name": "Pontificial Catholic University of Valparaiso",
        "institution_id": 4210116133,
        "raw_bridge_rows": 53
      },
      {
        "display_name": "ZHAW Zurich University of Applied Sciences",
        "institution_id": 200744771,
        "raw_bridge_rows": 50
      },
      {
        "display_name": "Federal University of S\u00e3o Jo\u00e3o del-Rei",
        "institution_id": 4210130985,
        "raw_bridge_rows": 41
      },
      {
        "display_name": "Universit\u00e9 Paul-Val\u00e9ry Montpellier",
        "institution_id": 4210095130,
        "raw_bridge_rows": 35
      },
      {
        "display_name": "Texas A&M Health Science Center",
        "institution_id": 4210105967,
        "raw_bridge_rows": 32
      },
      {
        "display_name": "Beibu Gulf University",
        "institution_id": 4210128032,
        "raw_bridge_rows": 30
      },
      {
        "display_name": "Parul University",
        "institution_id": 4210112983,
        "raw_bridge_rows": 29
      },
      {
        "display_name": "Indonesia Open University",
        "institution_id": 4210132268,
        "raw_bridge_rows": 27
      },
      {
        "display_name": "Spanish National Centre for Cardiovascular Research",
        "institution_id": 4210130400,
        "raw_bridge_rows": 26
      },
      {
        "display_name": "Instituto Superior de Contabilidade e Administracao do Porto",
        "institution_id": 11193315,
        "raw_bridge_rows": 25
      },
      {
        "display_name": "Iscte \u2013 Instituto Universit\u00e1rio de Lisboa",
        "institution_id": 4210100009,
        "raw_bridge_rows": 25
      },
      {
        "display_name": "Hospital de Sabadell",
        "institution_id": 4210124707,
        "raw_bridge_rows": 25
      }
    ],
    "normalized_sha256": "c0aa0cfc9c79716d2c257935daa062ec1a1dca2c5f13ada407b14282e398d8b0",
    "queries": [
      {
        "name": "raw_work_rows",
        "result_row_count": 1,
        "result_sha256": "74a4b54bd6c6fe3b72ff60e9d31fff2d02e1622bd0a05fa63ef21325131ac1b5",
        "sql": "SELECT count() AS rows, uniqExact(id) AS unique_ids FROM file('tiers/stage2_small/works/*.parquet', Parquet)",
        "sql_sha256": "12798bc7da425a178465fd84b4f92cc108f625159d50f2fcafce095c016ab67d"
      },
      {
        "name": "raw_bridge_counts",
        "result_row_count": 1,
        "result_sha256": "9192da1cdf9b0b667d34e46c464d9e90df1acb24afb44478aac0e0e6c2df72b7",
        "sql": "SELECT (SELECT count() FROM file('tiers/stage2_small/works/*.parquet', Parquet) ARRAY JOIN authorships AS a WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(a.author.id) IS NOT NULL) AS authors, (SELECT uniqExact(tuple(openalex_numeric_id(id), openalex_numeric_id(a.author.id), openalex_numeric_id(i.id))) FROM file('tiers/stage2_small/works/*.parquet', Parquet) ARRAY JOIN authorships AS a ARRAY JOIN a.institutions AS i WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(a.author.id) IS NOT NULL AND openalex_numeric_id(i.id) IS NOT NULL) AS institutions, (SELECT count() FROM file('tiers/stage2_small/works/*.parquet', Parquet) ARRAY JOIN topics AS t WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(t.id) IS NOT NULL AND t.score IS NOT NULL) AS topics",
        "sql_sha256": "554b0bd27e749b0e297df59df5b6f12493921c990072dd35aea134f2ad2b93fd"
      },
      {
        "name": "materialized_counts",
        "result_row_count": 1,
        "result_sha256": "29acd2fe9a3249f999b497fd2dcc5506f705281dd59d3fdb5bed85e18587b25b",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.works) AS works, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author) AS authors, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution) AS institutions, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_topic) AS topics, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.citation_edge) AS citations",
        "sql_sha256": "1034bcd28d120a2027a77515894dca5779123edf6979498d4cede4817949581d"
      },
      {
        "name": "referential_coverage",
        "result_row_count": 1,
        "result_sha256": "aaacea8bab04a1689cbd1580515b55fb7b21aa9a3ec549a22df8b6c55a6add54",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.works w ON wa.work_id=w.work_id) AS missing_works_for_authors, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author) AS author_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id) AS missing_authors, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id) AS distinct_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id) AS works_with_missing_authors, if(author_bridge_rows = 0, 1., 1 - missing_authors / author_bridge_rows) AS author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author WHERE author_id=9999999999) AS null_author_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author WHERE author_id=5317838346) AS deleted_author_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author WHERE author_id NOT IN (9999999999,5317838346)) AS ordinary_authorship_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS ordinary_missing_author_rows, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS distinct_ordinary_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS works_with_ordinary_missing_authors, if(ordinary_authorship_rows = 0, 1., 1 - ordinary_missing_author_rows / ordinary_authorship_rows) AS ordinary_author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution) AS institution_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) AS missing_institutions, (SELECT uniqExact(wi.institution_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) AS distinct_missing_institution_ids, (SELECT uniqExact(wi.work_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) AS works_with_missing_institutions, (SELECT uniqExact(wi.author_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) AS authors_with_missing_institutions, if(institution_bridge_rows = 0, 1., (institution_bridge_rows - missing_institutions) / institution_bridge_rows) AS institution_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_topic) AS topic_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.topics t ON wt.topic_id=t.topic_id) AS missing_topics, (SELECT uniqExact(wt.topic_id) FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.topics t ON wt.topic_id=t.topic_id) AS distinct_missing_topic_ids, if(topic_bridge_rows = 0, 1., (topic_bridge_rows - missing_topics) / topic_bridge_rows) AS topic_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.citation_edge) AS citation_edges, (SELECT count() FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.citation_edge ce INNER JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.works w ON ce.cited_work_id=w.work_id) AS retained_cited_edges, if(citation_edges = 0, 1., retained_cited_edges / citation_edges) AS citation_retention_ratio",
        "sql_sha256": "1798f1e6655531fb6188577d88d93bdd964bb00992efdcf1a64ad60d1e72f999"
      },
      {
        "name": "missing_author_sample",
        "result_row_count": 14,
        "result_sha256": "99a76bcebd2eb596aad11499de36d0f0433fdd046319d0bec9237a41f9f28082",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wa.author_id FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.authors a ON wa.author_id=a.author_id) SELECT openalex_numeric_id(authorship.author.id) AS author_id, multiIf(author_id=9999999999, 'null_author', author_id=5317838346, 'deleted_author', 'ordinary') AS classification, arraySlice(arraySort(groupUniqArray(ifNull(authorship.author.display_name, ''))), 1, 5) AS display_names, count() AS raw_bridge_rows FROM file('tiers/stage2_small/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship WHERE openalex_numeric_id(authorship.author.id) IN missing_ids GROUP BY author_id ORDER BY raw_bridge_rows DESC, author_id LIMIT 25",
        "sql_sha256": "bddfc4ac65ed21105be0d06e0311da6735b4f771ddc69a9c62d1ed26fa196a64"
      },
      {
        "name": "missing_institution_sample",
        "result_row_count": 25,
        "result_sha256": "e76891d77558501c47c0f69c20680983202e0d65482fb85bfcbd131b4f66f365",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wi.institution_id FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions i ON wi.institution_id=i.institution_id) SELECT openalex_numeric_id(raw_institution.id) AS institution_id, any(raw_institution.display_name) AS display_name, count() AS raw_bridge_rows FROM file('tiers/stage2_small/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship ARRAY JOIN authorship.institutions AS raw_institution WHERE openalex_numeric_id(raw_institution.id) IN missing_ids GROUP BY institution_id ORDER BY raw_bridge_rows DESC, institution_id LIMIT 25",
        "sql_sha256": "8fcc9cdc4577ab85ecbb115fa3694bc17453a0f7fb981d82d9043e6cc792399f"
      },
      {
        "name": "works_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "74a4b54bd6c6fe3b72ff60e9d31fff2d02e1622bd0a05fa63ef21325131ac1b5",
        "sql": "SELECT count() AS rows, uniqExact(work_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.works",
        "sql_sha256": "a54c0fb3d18dcd02ed53a840790d7973e1dc8170eea48ea4335d20b35d299679"
      },
      {
        "name": "authors_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "ad147b0c2afdbf81139c75c21696b85568b9bd6db2c30818e5fe0d962e8a0170",
        "sql": "SELECT count() AS rows, uniqExact(author_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.authors",
        "sql_sha256": "200051495727abc3514bed465df41bebe27c063b6fee465fe23ef469dd8dbf85"
      },
      {
        "name": "institutions_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "1d729a2ea001d72722af893931308d2a7ffb55562e2a5a3c33945a1cc15f9c47",
        "sql": "SELECT count() AS rows, uniqExact(institution_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.institutions",
        "sql_sha256": "757a66a097fa2d64b91dc2421042c308344cb73c5357fadbeda04642fdee8c88"
      },
      {
        "name": "sources_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "8515fa4a030ad72ca441f50ae103ac1b7701fb65366d5de9dab09a297ce71e9f",
        "sql": "SELECT count() AS rows, uniqExact(source_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.sources",
        "sql_sha256": "2cffeeefb3c19dc9d29bcc96b418636c52a72ad1211d0129f663c3b0930a14f7"
      },
      {
        "name": "topics_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "83708a811c93190b16a1b7dbe7033261c7a31e9cc7d70ade69ae253c50e5ac75",
        "sql": "SELECT count() AS rows, uniqExact(topic_id) AS unique_ids FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.topics",
        "sql_sha256": "ce4bf89d0bfd351946fa215f3e6d8b843c16a9000c3634036880e73fc02472a8"
      },
      {
        "name": "year_type_topic_xpac_distribution",
        "result_row_count": 492399,
        "result_sha256": "89b42e728db3c8983e10ef0e5324c51deb698afea5daa05dcefcf53b0917024e",
        "sql": "SELECT publication_year, work_type, primary_topic_id, is_xpac, count() AS works FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.works GROUP BY ALL ORDER BY ALL",
        "sql_sha256": "1ef536038c3b3b49ba3d50fee3df969241d692eae667c87e94fae1acdec18aa6"
      },
      {
        "name": "authorships_per_work",
        "result_row_count": 200,
        "result_sha256": "8c704127e6d040ac4779ce338b625f61ecd0f9a7faee500ee1f59850b8dc3b38",
        "sql": "SELECT authorships, count() AS works FROM (SELECT work_id, count() AS authorships FROM openalex_stage2_stage2_instrumented_18c1_4c76305e.work_author GROUP BY work_id) GROUP BY authorships ORDER BY authorships",
        "sql_sha256": "8f0630e0c24ae39834589df78b9ec41c24f32100d26af4debaf0ba9e3dd7db22"
      }
    ],
    "raw_evidence": {
      "distinct_valid_pairs": 15283016,
      "duplicate_pair_delta": 0,
      "null_topic_scores": 0,
      "raw_reference_entries": 15283016,
      "rejected_id_entries": 0
    },
    "referential_coverage": {
      "author_bridge_rows": 3852081,
      "author_reference_coverage_ratio": 0.9978886736805379,
      "authors_with_missing_institutions": 2980,
      "citation_edges": 15283016,
      "citation_retention_ratio": 0.005086299719898219,
      "deleted_author_rows": 0,
      "distinct_missing_author_ids": 14,
      "distinct_missing_institution_ids": 122,
      "distinct_missing_topic_ids": 0,
      "distinct_ordinary_missing_author_ids": 13,
      "institution_bridge_rows": 2646224,
      "institution_reference_coverage_ratio": 0.9988160488303334,
      "missing_authors": 8133,
      "missing_institutions": 3133,
      "missing_topics": 0,
      "missing_works_for_authors": 0,
      "null_author_rows": 8118,
      "ordinary_author_reference_coverage_ratio": 0.9999960977772159,
      "ordinary_authorship_rows": 3843963,
      "ordinary_missing_author_rows": 15,
      "retained_cited_edges": 77734,
      "topic_bridge_rows": 4139113,
      "topic_reference_coverage_ratio": 1,
      "works_with_missing_authors": 8117,
      "works_with_missing_institutions": 1501,
      "works_with_ordinary_missing_authors": 14
    },
    "sql_sha256": {
      "05_raw_evidence.sql": "797a7ccfaecba47b213e1664e925a39e284aeed47a89b71106934db9f0950681",
      "20_load_works.sql": "731fcec7e55121827dee7f1806feffe213c322d67754b14a4dd1c4ea7f674144"
    }
  }
}
```

## Sequential and concurrent evidence

```json
{
  "concurrent": {
    "stage2_large": {
      "classes": {
        "join": {
          "count": 150,
          "insufficient_sample": false,
          "maximum_seconds": 66.27,
          "median_seconds": 12.861,
          "p95_seconds": 64.816,
          "peak_memory_bytes": 4825824496,
          "read_bytes": 375047789600,
          "read_rows": 20522546850,
          "spill_bytes": 0
        },
        "one_hop": {
          "count": 50,
          "insufficient_sample": false,
          "maximum_seconds": 0.248,
          "median_seconds": 0.012,
          "p95_seconds": 0.018,
          "peak_memory_bytes": 5799875,
          "read_bytes": 1735931208,
          "read_rows": 215275251,
          "spill_bytes": 0
        },
        "routine": {
          "count": 99,
          "insufficient_sample": false,
          "maximum_seconds": 6.049,
          "median_seconds": 0.064,
          "p95_seconds": 5.213,
          "peak_memory_bytes": 6477911021,
          "read_bytes": 122101866093,
          "read_rows": 11824834213,
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
        "completed_merge_count": 5678,
        "completed_system_merge_count": 5677,
        "in_flight_benchmark_merge_count": 0,
        "in_flight_merge_count": 0,
        "in_flight_system_merge_count": 0,
        "maximum_completed_merge_ms": 8861,
        "maximum_completed_system_merge_ms": 7890,
        "part_log_coverage": {
          "maximum_event_at_unix_us": 1785981148760215,
          "minimum_event_at_unix_us": 1785868945280710,
          "row_count": 47833
        },
        "schema_version": 1,
        "status": "complete"
      },
      "queries": {
        "q01": {
          "count": 50,
          "maximum_seconds": 0.064,
          "median_seconds": 0.056,
          "p95_seconds": 0.061,
          "peak_memory_bytes": 123337851,
          "spill_bytes": 0
        },
        "q02": {
          "count": 50,
          "maximum_seconds": 66.27,
          "median_seconds": 62.22,
          "p95_seconds": 65.365,
          "peak_memory_bytes": 4432201863,
          "spill_bytes": 0
        },
        "q03": {
          "count": 50,
          "maximum_seconds": 11.384,
          "median_seconds": 10.401,
          "p95_seconds": 10.796,
          "peak_memory_bytes": 4653208668,
          "spill_bytes": 0
        },
        "q04": {
          "count": 50,
          "maximum_seconds": 13.995,
          "median_seconds": 12.861,
          "p95_seconds": 13.449,
          "peak_memory_bytes": 4825824496,
          "spill_bytes": 0
        },
        "q05": {
          "count": 50,
          "maximum_seconds": 0.248,
          "median_seconds": 0.012,
          "p95_seconds": 0.018,
          "peak_memory_bytes": 5799875,
          "spill_bytes": 0
        },
        "q07": {
          "count": 49,
          "maximum_seconds": 6.049,
          "median_seconds": 4.879,
          "p95_seconds": 5.355,
          "peak_memory_bytes": 6477911021,
          "spill_bytes": 0
        }
      },
      "server_restarted": false,
      "verdict_cap": "pass"
    },
    "stage2_medium": {
      "classes": {
        "join": {
          "count": 150,
          "insufficient_sample": false,
          "maximum_seconds": 10.815,
          "median_seconds": 2.876,
          "p95_seconds": 10.367,
          "peak_memory_bytes": 4538044210,
          "read_bytes": 227563532400,
          "read_rows": 10624296150,
          "spill_bytes": 0
        },
        "one_hop": {
          "count": 50,
          "insufficient_sample": false,
          "maximum_seconds": 0.084,
          "median_seconds": 0.006,
          "p95_seconds": 0.01,
          "peak_memory_bytes": 2173270,
          "read_bytes": 574721872,
          "read_rows": 71235184,
          "spill_bytes": 0
        },
        "routine": {
          "count": 99,
          "insufficient_sample": false,
          "maximum_seconds": 1.686,
          "median_seconds": 0.039,
          "p95_seconds": 1.571,
          "peak_memory_bytes": 6516324092,
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
        "completed_merge_count": 830,
        "completed_system_merge_count": 830,
        "in_flight_benchmark_merge_count": 0,
        "in_flight_merge_count": 0,
        "in_flight_system_merge_count": 0,
        "maximum_completed_merge_ms": 672,
        "maximum_completed_system_merge_ms": 672,
        "part_log_coverage": {
          "maximum_event_at_unix_us": 1785975795998402,
          "minimum_event_at_unix_us": 1785868945280710,
          "row_count": 41631
        },
        "schema_version": 1,
        "status": "complete"
      },
      "queries": {
        "q01": {
          "count": 50,
          "maximum_seconds": 0.039,
          "median_seconds": 0.026,
          "p95_seconds": 0.03,
          "peak_memory_bytes": 122834149,
          "spill_bytes": 0
        },
        "q02": {
          "count": 50,
          "maximum_seconds": 10.815,
          "median_seconds": 10.073,
          "p95_seconds": 10.681,
          "peak_memory_bytes": 3074541239,
          "spill_bytes": 0
        },
        "q03": {
          "count": 50,
          "maximum_seconds": 3.045,
          "median_seconds": 2.874,
          "p95_seconds": 2.968,
          "peak_memory_bytes": 4538044210,
          "spill_bytes": 0
        },
        "q04": {
          "count": 50,
          "maximum_seconds": 2.981,
          "median_seconds": 2.717,
          "p95_seconds": 2.888,
          "peak_memory_bytes": 2280955910,
          "spill_bytes": 0
        },
        "q05": {
          "count": 50,
          "maximum_seconds": 0.084,
          "median_seconds": 0.006,
          "p95_seconds": 0.01,
          "peak_memory_bytes": 2173270,
          "spill_bytes": 0
        },
        "q07": {
          "count": 49,
          "maximum_seconds": 1.686,
          "median_seconds": 1.494,
          "p95_seconds": 1.588,
          "peak_memory_bytes": 6516324092,
          "spill_bytes": 0
        }
      },
      "server_restarted": false,
      "verdict_cap": "pass"
    },
    "stage2_small": {
      "classes": {
        "join": {
          "count": 150,
          "insufficient_sample": false,
          "maximum_seconds": 0.975,
          "median_seconds": 0.341,
          "p95_seconds": 0.858,
          "peak_memory_bytes": 2451053278,
          "read_bytes": 172574035100,
          "read_rows": 6934116600,
          "spill_bytes": 0
        },
        "one_hop": {
          "count": 50,
          "insufficient_sample": false,
          "maximum_seconds": 0.023,
          "median_seconds": 0.003,
          "p95_seconds": 0.004,
          "peak_memory_bytes": 849516,
          "read_bytes": 136132864,
          "read_rows": 16929608,
          "spill_bytes": 0
        },
        "routine": {
          "count": 99,
          "insufficient_sample": false,
          "maximum_seconds": 0.176,
          "median_seconds": 0.027,
          "p95_seconds": 0.171,
          "peak_memory_bytes": 1813494357,
          "read_bytes": 8838440224,
          "read_rows": 849016884,
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
        "completed_merge_count": 480,
        "completed_system_merge_count": 480,
        "in_flight_benchmark_merge_count": 0,
        "in_flight_merge_count": 0,
        "in_flight_system_merge_count": 0,
        "maximum_completed_merge_ms": 3232,
        "maximum_completed_system_merge_ms": 3232,
        "part_log_coverage": {
          "maximum_event_at_unix_us": 1785974589971987,
          "minimum_event_at_unix_us": 1785868945280710,
          "row_count": 40621
        },
        "schema_version": 1,
        "status": "complete"
      },
      "queries": {
        "q01": {
          "count": 50,
          "maximum_seconds": 0.027,
          "median_seconds": 0.013,
          "p95_seconds": 0.016,
          "peak_memory_bytes": 68503329,
          "spill_bytes": 0
        },
        "q02": {
          "count": 50,
          "maximum_seconds": 0.265,
          "median_seconds": 0.256,
          "p95_seconds": 0.263,
          "peak_memory_bytes": 1158249068,
          "spill_bytes": 0
        },
        "q03": {
          "count": 50,
          "maximum_seconds": 0.975,
          "median_seconds": 0.838,
          "p95_seconds": 0.874,
          "peak_memory_bytes": 2451053278,
          "spill_bytes": 0
        },
        "q04": {
          "count": 50,
          "maximum_seconds": 0.375,
          "median_seconds": 0.341,
          "p95_seconds": 0.366,
          "peak_memory_bytes": 687535482,
          "spill_bytes": 0
        },
        "q05": {
          "count": 50,
          "maximum_seconds": 0.023,
          "median_seconds": 0.003,
          "p95_seconds": 0.004,
          "peak_memory_bytes": 849516,
          "spill_bytes": 0
        },
        "q07": {
          "count": 49,
          "maximum_seconds": 0.176,
          "median_seconds": 0.156,
          "p95_seconds": 0.174,
          "peak_memory_bytes": 1813494357,
          "spill_bytes": 0
        }
      },
      "server_restarted": false,
      "verdict_cap": "pass"
    }
  },
  "sequential": {
    "stage2_large": [
      {
        "disk_read_elapsed_us": 422170,
        "elapsed_seconds": 0.146,
        "file_descriptor_read_bytes": 26394388,
        "finished_at_unix_us": 1785975915096208,
        "gating": true,
        "os_cpu_virtual_time_us": 651426,
        "os_cpu_wait_time_us": 118515,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 26394388,
        "page_cache_miss_elapsed_us": 421319,
        "peak_memory_bytes": 122117113,
        "query_class": "routine",
        "query_id": "df512afc-6dbe-5945-a5d1-e55bf577bf44",
        "query_name": "q01",
        "read_bytes": 191311446,
        "read_rows": 31885241,
        "real_time_us": 3408378,
        "result_rows": 11928,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785975914950318,
        "synchronous_read_wait_us": 924093,
        "system_time_us": 41510,
        "user_time_us": 610587
      },
      {
        "disk_read_elapsed_us": 344658,
        "elapsed_seconds": 0.102,
        "file_descriptor_read_bytes": 26305370,
        "finished_at_unix_us": 1785975915847295,
        "gating": true,
        "os_cpu_virtual_time_us": 646630,
        "os_cpu_wait_time_us": 124782,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 26305370,
        "page_cache_miss_elapsed_us": 343956,
        "peak_memory_bytes": 121549629,
        "query_class": "routine",
        "query_id": "daf2a53e-c750-5e2f-860b-e1505cfea366",
        "query_name": "q01",
        "read_bytes": 191311446,
        "read_rows": 31885241,
        "real_time_us": 2372451,
        "result_rows": 11928,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785975915744687,
        "synchronous_read_wait_us": 781584,
        "system_time_us": 41369,
        "user_time_us": 605748
      },
      {
        "disk_read_elapsed_us": 328488,
        "elapsed_seconds": 0.093,
        "file_descriptor_read_bytes": 26041001,
        "finished_at_unix_us": 1785975916561819,
        "gating": true,
        "os_cpu_virtual_time_us": 642617,
        "os_cpu_wait_time_us": 114952,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 26041001,
        "page_cache_miss_elapsed_us": 327146,
        "peak_memory_bytes": 121187478,
        "query_class": "routine",
        "query_id": "d3bb4593-4c92-5135-a170-ffa8c6570ed0",
        "query_name": "q01",
        "read_bytes": 191311446,
        "read_rows": 31885241,
        "real_time_us": 2160182,
        "result_rows": 11928,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785975916468732,
        "synchronous_read_wait_us": 544225,
        "system_time_us": 38629,
        "user_time_us": 604430
      },
      {
        "disk_read_elapsed_us": 56389,
        "elapsed_seconds": 0.057,
        "file_descriptor_read_bytes": 26751570,
        "finished_at_unix_us": 1785975917017964,
        "gating": true,
        "os_cpu_virtual_time_us": 651247,
        "os_cpu_wait_time_us": 67491,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 26751570,
        "page_cache_miss_elapsed_us": 55629,
        "peak_memory_bytes": 120729826,
        "query_class": "routine",
        "query_id": "5a32df48-5741-5587-ac89-9ce3aba1a9ab",
        "query_name": "q01",
        "read_bytes": 191311446,
        "read_rows": 31885241,
        "real_time_us": 1168072,
        "result_rows": 11928,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785975916961023,
        "synchronous_read_wait_us": 208561,
        "system_time_us": 25978,
        "user_time_us": 625817
      },
      {
        "disk_read_elapsed_us": 53887,
        "elapsed_seconds": 0.056,
        "file_descriptor_read_bytes": 26207621,
        "finished_at_unix_us": 1785975917473122,
        "gating": true,
        "os_cpu_virtual_time_us": 656397,
        "os_cpu_wait_time_us": 58733,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 26207621,
        "page_cache_miss_elapsed_us": 52894,
        "peak_memory_bytes": 120672005,
        "query_class": "routine",
        "query_id": "e04f25c3-0733-5e23-9720-f93eefba728d",
        "query_name": "q01",
        "read_bytes": 191311446,
        "read_rows": 31885241,
        "real_time_us": 1144014,
        "result_rows": 11928,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785975917417246,
        "synchronous_read_wait_us": 184691,
        "system_time_us": 38117,
        "user_time_us": 618723
      },
      {
        "disk_read_elapsed_us": 52107,
        "elapsed_seconds": 0.055,
        "file_descriptor_read_bytes": 26199570,
        "finished_at_unix_us": 1785975917905823,
        "gating": true,
        "os_cpu_virtual_time_us": 644961,
        "os_cpu_wait_time_us": 56570,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 26199570,
        "page_cache_miss_elapsed_us": 51337,
        "peak_memory_bytes": 120668757,
        "query_class": "routine",
        "query_id": "3f5f661e-7b16-5e6b-8061-a243b02826cf",
        "query_name": "q01",
        "read_bytes": 191311446,
        "read_rows": 31885241,
        "real_time_us": 1121490,
        "result_rows": 11928,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785975917851006,
        "synchronous_read_wait_us": 179406,
        "system_time_us": 20573,
        "user_time_us": 624832
      },
      {
        "disk_read_elapsed_us": 123734814,
        "elapsed_seconds": 61.662,
        "file_descriptor_read_bytes": 101041803870,
        "finished_at_unix_us": 1785975989124103,
        "gating": true,
        "os_cpu_virtual_time_us": 220603272,
        "os_cpu_wait_time_us": 77266572,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 556436158,
        "page_cache_miss_elapsed_us": 665913,
        "peak_memory_bytes": 4357313055,
        "query_class": "join",
        "query_id": "13595f55-8ce6-5f96-9afd-a4a8889d126a",
        "query_name": "q02",
        "read_bytes": 1511924436,
        "read_rows": 96479335,
        "real_time_us": 1229306542,
        "result_rows": 838464,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785975927708413,
        "synchronous_read_wait_us": 1123945,
        "system_time_us": 45353613,
        "user_time_us": 175250639
      },
      {
        "disk_read_elapsed_us": 98014885,
        "elapsed_seconds": 60.114,
        "file_descriptor_read_bytes": 93387972837,
        "finished_at_unix_us": 1785976049620795,
        "gating": true,
        "os_cpu_virtual_time_us": 194927636,
        "os_cpu_wait_time_us": 78684861,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 556509784,
        "page_cache_miss_elapsed_us": 678977,
        "peak_memory_bytes": 4358421483,
        "query_class": "join",
        "query_id": "a2848046-3ec2-5022-963e-ecd8f76e25e6",
        "query_name": "q02",
        "read_bytes": 1511924436,
        "read_rows": 96479335,
        "real_time_us": 1198567385,
        "result_rows": 838464,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785975989734466,
        "synchronous_read_wait_us": 1044222,
        "system_time_us": 39122422,
        "user_time_us": 155808256
      },
      {
        "disk_read_elapsed_us": 115962619,
        "elapsed_seconds": 60.025,
        "file_descriptor_read_bytes": 99334299195,
        "finished_at_unix_us": 1785976110035102,
        "gating": true,
        "os_cpu_virtual_time_us": 209001976,
        "os_cpu_wait_time_us": 77779766,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 556197410,
        "page_cache_miss_elapsed_us": 625496,
        "peak_memory_bytes": 4328054399,
        "query_class": "join",
        "query_id": "5504b261-1dca-5b3c-a586-47a9e9403c20",
        "query_name": "q02",
        "read_bytes": 1511924436,
        "read_rows": 96479335,
        "real_time_us": 1196650782,
        "result_rows": 838464,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976050243035,
        "synchronous_read_wait_us": 989792,
        "system_time_us": 44039116,
        "user_time_us": 164965752
      },
      {
        "disk_read_elapsed_us": 112486731,
        "elapsed_seconds": 59.889,
        "file_descriptor_read_bytes": 101149471897,
        "finished_at_unix_us": 1785976170275557,
        "gating": true,
        "os_cpu_virtual_time_us": 210846731,
        "os_cpu_wait_time_us": 81069228,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 556227335,
        "page_cache_miss_elapsed_us": 651378,
        "peak_memory_bytes": 4380036610,
        "query_class": "join",
        "query_id": "edd03e6a-5f6b-5a3c-9c5b-bc50f3eddaad",
        "query_name": "q02",
        "read_bytes": 1511924436,
        "read_rows": 96479335,
        "real_time_us": 1193458824,
        "result_rows": 838464,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976110638915,
        "synchronous_read_wait_us": 1022856,
        "system_time_us": 45429639,
        "user_time_us": 165420041
      },
      {
        "disk_read_elapsed_us": 118511642,
        "elapsed_seconds": 60.45,
        "file_descriptor_read_bytes": 102763698276,
        "finished_at_unix_us": 1785976231112445,
        "gating": true,
        "os_cpu_virtual_time_us": 215698714,
        "os_cpu_wait_time_us": 79341577,
        "os_read_bytes": 4096,
        "page_cache_miss_bytes": 556239369,
        "page_cache_miss_elapsed_us": 670494,
        "peak_memory_bytes": 4359557150,
        "query_class": "join",
        "query_id": "bfad4687-cb42-5ffe-bbec-e399dc66ffac",
        "query_name": "q02",
        "read_bytes": 1511924436,
        "read_rows": 96479335,
        "real_time_us": 1205074480,
        "result_rows": 838464,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976170900729,
        "synchronous_read_wait_us": 1035138,
        "system_time_us": 47430820,
        "user_time_us": 168270924
      },
      {
        "disk_read_elapsed_us": 102997974,
        "elapsed_seconds": 60.001,
        "file_descriptor_read_bytes": 96061731759,
        "finished_at_unix_us": 1785976291523429,
        "gating": true,
        "os_cpu_virtual_time_us": 201652117,
        "os_cpu_wait_time_us": 80440219,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 556396297,
        "page_cache_miss_elapsed_us": 644716,
        "peak_memory_bytes": 4335000048,
        "query_class": "join",
        "query_id": "c63b7a6c-1bb7-5a2d-8f4b-edc4eb13fe71",
        "query_name": "q02",
        "read_bytes": 1511924436,
        "read_rows": 96479335,
        "real_time_us": 1195318678,
        "result_rows": 838464,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976231803443,
        "synchronous_read_wait_us": 1005392,
        "system_time_us": 43033840,
        "user_time_us": 158621220
      },
      {
        "disk_read_elapsed_us": 4324022,
        "elapsed_seconds": 9.41,
        "file_descriptor_read_bytes": 4835587405,
        "finished_at_unix_us": 1785976311732058,
        "gating": true,
        "os_cpu_virtual_time_us": 41532272,
        "os_cpu_wait_time_us": 2564298,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 3132135938,
        "page_cache_miss_elapsed_us": 2581326,
        "peak_memory_bytes": 4533689059,
        "query_class": "join",
        "query_id": "55a2bf14-7bc6-50bb-b8f8-e7afc7b5a6d8",
        "query_name": "q03",
        "read_bytes": 4369474957,
        "read_rows": 202831399,
        "real_time_us": 187413149,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976302512102,
        "synchronous_read_wait_us": 7084720,
        "system_time_us": 2549889,
        "user_time_us": 38993644
      },
      {
        "disk_read_elapsed_us": 4252803,
        "elapsed_seconds": 9.799,
        "file_descriptor_read_bytes": 4832275079,
        "finished_at_unix_us": 1785976321890445,
        "gating": true,
        "os_cpu_virtual_time_us": 42505928,
        "os_cpu_wait_time_us": 2614565,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 3129950513,
        "page_cache_miss_elapsed_us": 2548093,
        "peak_memory_bytes": 4455711795,
        "query_class": "join",
        "query_id": "68b45e30-86bb-5487-9691-09331c63a648",
        "query_name": "q03",
        "read_bytes": 4369474957,
        "read_rows": 202831399,
        "real_time_us": 195010141,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976312285606,
        "synchronous_read_wait_us": 6477590,
        "system_time_us": 2660303,
        "user_time_us": 39855849
      },
      {
        "disk_read_elapsed_us": 4388510,
        "elapsed_seconds": 10.797,
        "file_descriptor_read_bytes": 4832635319,
        "finished_at_unix_us": 1785976332898702,
        "gating": true,
        "os_cpu_virtual_time_us": 43425754,
        "os_cpu_wait_time_us": 2585035,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 3128699394,
        "page_cache_miss_elapsed_us": 2517551,
        "peak_memory_bytes": 4465035999,
        "query_class": "join",
        "query_id": "c3ea97aa-7c10-5851-805d-648e39c76f4d",
        "query_name": "q03",
        "read_bytes": 4369474957,
        "read_rows": 202831399,
        "real_time_us": 212080358,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976322447969,
        "synchronous_read_wait_us": 6618881,
        "system_time_us": 3007139,
        "user_time_us": 40430982
      },
      {
        "disk_read_elapsed_us": 4169778,
        "elapsed_seconds": 9.947,
        "file_descriptor_read_bytes": 4832231199,
        "finished_at_unix_us": 1785976343405809,
        "gating": true,
        "os_cpu_virtual_time_us": 43525580,
        "os_cpu_wait_time_us": 2594902,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 3128894874,
        "page_cache_miss_elapsed_us": 2486344,
        "peak_memory_bytes": 4388389438,
        "query_class": "join",
        "query_id": "02ca305d-ad37-5cb1-a79a-a037ed6dc1df",
        "query_name": "q03",
        "read_bytes": 4369474957,
        "read_rows": 202831399,
        "real_time_us": 198033412,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976333645777,
        "synchronous_read_wait_us": 6523814,
        "system_time_us": 2957429,
        "user_time_us": 40579986
      },
      {
        "disk_read_elapsed_us": 4193483,
        "elapsed_seconds": 9.893,
        "file_descriptor_read_bytes": 4831181364,
        "finished_at_unix_us": 1785976353618813,
        "gating": true,
        "os_cpu_virtual_time_us": 43374877,
        "os_cpu_wait_time_us": 2605001,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 3130212657,
        "page_cache_miss_elapsed_us": 2465989,
        "peak_memory_bytes": 4510496897,
        "query_class": "join",
        "query_id": "5e44ed1a-1a6c-53c4-963f-15b1773e443c",
        "query_name": "q03",
        "read_bytes": 4369474957,
        "read_rows": 202831399,
        "real_time_us": 196463751,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976343940084,
        "synchronous_read_wait_us": 6562013,
        "system_time_us": 2992532,
        "user_time_us": 40394363
      },
      {
        "disk_read_elapsed_us": 4266881,
        "elapsed_seconds": 9.993,
        "file_descriptor_read_bytes": 4830391357,
        "finished_at_unix_us": 1785976364010251,
        "gating": true,
        "os_cpu_virtual_time_us": 43599325,
        "os_cpu_wait_time_us": 2734643,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 3129092610,
        "page_cache_miss_elapsed_us": 2464743,
        "peak_memory_bytes": 4419294623,
        "query_class": "join",
        "query_id": "940ad897-60ba-5c49-9760-e4c1df1d7253",
        "query_name": "q03",
        "read_bytes": 4369474957,
        "read_rows": 202831399,
        "real_time_us": 199011765,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976354201899,
        "synchronous_read_wait_us": 6521671,
        "system_time_us": 3094533,
        "user_time_us": 40516673
      },
      {
        "disk_read_elapsed_us": 414513,
        "elapsed_seconds": 11.305,
        "file_descriptor_read_bytes": 435166516,
        "finished_at_unix_us": 1785976385418583,
        "gating": true,
        "os_cpu_virtual_time_us": 23792308,
        "os_cpu_wait_time_us": 144080,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 410478711,
        "page_cache_miss_elapsed_us": 359077,
        "peak_memory_bytes": 4813240679,
        "query_class": "join",
        "query_id": "7ba2143e-1129-5b61-aa62-5815d203c396",
        "query_name": "q04",
        "read_bytes": 1619556399,
        "read_rows": 111140203,
        "real_time_us": 225883504,
        "result_rows": 173617,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976374130288,
        "synchronous_read_wait_us": 649890,
        "system_time_us": 437955,
        "user_time_us": 23356868
      },
      {
        "disk_read_elapsed_us": 234493,
        "elapsed_seconds": 11.424,
        "file_descriptor_read_bytes": 435031644,
        "finished_at_unix_us": 1785976397221581,
        "gating": true,
        "os_cpu_virtual_time_us": 24143898,
        "os_cpu_wait_time_us": 191298,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 410431503,
        "page_cache_miss_elapsed_us": 201483,
        "peak_memory_bytes": 4816155534,
        "query_class": "join",
        "query_id": "cedb075c-63d5-5b0e-95b3-395ba6ca4d9a",
        "query_name": "q04",
        "read_bytes": 1619556399,
        "read_rows": 111140203,
        "real_time_us": 228257388,
        "result_rows": 173617,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976385814396,
        "synchronous_read_wait_us": 483573,
        "system_time_us": 386729,
        "user_time_us": 23759743
      },
      {
        "disk_read_elapsed_us": 223146,
        "elapsed_seconds": 11.722,
        "file_descriptor_read_bytes": 435073604,
        "finished_at_unix_us": 1785976409307461,
        "gating": true,
        "os_cpu_virtual_time_us": 24852534,
        "os_cpu_wait_time_us": 162731,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 410483728,
        "page_cache_miss_elapsed_us": 187278,
        "peak_memory_bytes": 4821043077,
        "query_class": "join",
        "query_id": "9801aa14-b9e6-5fd2-b51f-036a8ddf9c9a",
        "query_name": "q04",
        "read_bytes": 1619556399,
        "read_rows": 111140203,
        "real_time_us": 234247937,
        "result_rows": 173617,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976397601212,
        "synchronous_read_wait_us": 470792,
        "system_time_us": 570122,
        "user_time_us": 24284822
      },
      {
        "disk_read_elapsed_us": 251049,
        "elapsed_seconds": 11.646,
        "file_descriptor_read_bytes": 435102022,
        "finished_at_unix_us": 1785976421324787,
        "gating": true,
        "os_cpu_virtual_time_us": 24308084,
        "os_cpu_wait_time_us": 539037,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 410483728,
        "page_cache_miss_elapsed_us": 216999,
        "peak_memory_bytes": 4815596294,
        "query_class": "join",
        "query_id": "cac9576c-5bbd-5797-b028-2d781cf4f7c1",
        "query_name": "q04",
        "read_bytes": 1619556399,
        "read_rows": 111140203,
        "real_time_us": 232744955,
        "result_rows": 173617,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976409695671,
        "synchronous_read_wait_us": 507437,
        "system_time_us": 508764,
        "user_time_us": 23801836
      },
      {
        "disk_read_elapsed_us": 240321,
        "elapsed_seconds": 11.592,
        "file_descriptor_read_bytes": 435203057,
        "finished_at_unix_us": 1785976433271001,
        "gating": true,
        "os_cpu_virtual_time_us": 24276682,
        "os_cpu_wait_time_us": 158977,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 410483728,
        "page_cache_miss_elapsed_us": 196529,
        "peak_memory_bytes": 4812859784,
        "query_class": "join",
        "query_id": "0810c65e-2c98-5cd1-b43c-bfb4c95a789a",
        "query_name": "q04",
        "read_bytes": 1619556399,
        "read_rows": 111140203,
        "real_time_us": 231596757,
        "result_rows": 173617,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976421695828,
        "synchronous_read_wait_us": 471490,
        "system_time_us": 509846,
        "user_time_us": 23769426
      },
      {
        "disk_read_elapsed_us": 234831,
        "elapsed_seconds": 11.693,
        "file_descriptor_read_bytes": 435019945,
        "finished_at_unix_us": 1785976445344087,
        "gating": true,
        "os_cpu_virtual_time_us": 24404262,
        "os_cpu_wait_time_us": 132821,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 410431503,
        "page_cache_miss_elapsed_us": 198753,
        "peak_memory_bytes": 4809003159,
        "query_class": "join",
        "query_id": "3b30e5aa-2e1a-5868-8c48-f7db737325cd",
        "query_name": "q04",
        "read_bytes": 1619556399,
        "read_rows": 111140203,
        "real_time_us": 233666915,
        "result_rows": 173617,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976433668011,
        "synchronous_read_wait_us": 489712,
        "system_time_us": 590361,
        "user_time_us": 23816447
      },
      {
        "disk_read_elapsed_us": 12965888,
        "elapsed_seconds": 0.856,
        "file_descriptor_read_bytes": 1221876148,
        "finished_at_unix_us": 1785976456500049,
        "gating": true,
        "os_cpu_virtual_time_us": 1532194,
        "os_cpu_wait_time_us": 127392,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1221657809,
        "page_cache_miss_elapsed_us": 12933420,
        "peak_memory_bytes": 5809608,
        "query_class": "one_hop",
        "query_id": "b730b9c4-9614-57b4-b429-efae8d8cca95",
        "query_name": "q05",
        "read_bytes": 1670821784,
        "read_rows": 208852723,
        "real_time_us": 30217699,
        "result_rows": 0,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976455644052,
        "synchronous_read_wait_us": 14169826,
        "system_time_us": 628670,
        "user_time_us": 910161
      },
      {
        "disk_read_elapsed_us": 2831608,
        "elapsed_seconds": 0.258,
        "file_descriptor_read_bytes": 1222454131,
        "finished_at_unix_us": 1785976457114388,
        "gating": true,
        "os_cpu_virtual_time_us": 1391163,
        "os_cpu_wait_time_us": 134124,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1222454131,
        "page_cache_miss_elapsed_us": 2827668,
        "peak_memory_bytes": 5791155,
        "query_class": "one_hop",
        "query_id": "4c447197-0298-5dcc-863c-bb68268e94b7",
        "query_name": "q05",
        "read_bytes": 1671096368,
        "read_rows": 208852723,
        "real_time_us": 8005941,
        "result_rows": 48,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976456855981,
        "synchronous_read_wait_us": 3682819,
        "system_time_us": 544138,
        "user_time_us": 851485
      },
      {
        "disk_read_elapsed_us": 2713777,
        "elapsed_seconds": 0.252,
        "file_descriptor_read_bytes": 1221989112,
        "finished_at_unix_us": 1785976457753154,
        "gating": true,
        "os_cpu_virtual_time_us": 1388571,
        "os_cpu_wait_time_us": 165479,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1221989112,
        "page_cache_miss_elapsed_us": 2708909,
        "peak_memory_bytes": 5865696,
        "query_class": "one_hop",
        "query_id": "cecc163f-7a64-5b1a-8a6b-67432d383cf3",
        "query_name": "q05",
        "read_bytes": 1671218272,
        "read_rows": 208852723,
        "real_time_us": 7772129,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976457500442,
        "synchronous_read_wait_us": 3592623,
        "system_time_us": 535217,
        "user_time_us": 857089
      },
      {
        "disk_read_elapsed_us": 0,
        "elapsed_seconds": 0.001,
        "file_descriptor_read_bytes": 0,
        "finished_at_unix_us": 1785976458105228,
        "gating": true,
        "os_cpu_virtual_time_us": 1073,
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
        "real_time_us": 1355,
        "result_rows": 0,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976458104089,
        "synchronous_read_wait_us": 0,
        "system_time_us": 896,
        "user_time_us": 180
      },
      {
        "disk_read_elapsed_us": 1730,
        "elapsed_seconds": 0.011,
        "file_descriptor_read_bytes": 1127883,
        "finished_at_unix_us": 1785976458467498,
        "gating": true,
        "os_cpu_virtual_time_us": 31948,
        "os_cpu_wait_time_us": 134,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1127883,
        "page_cache_miss_elapsed_us": 1719,
        "peak_memory_bytes": 448763,
        "query_class": "one_hop",
        "query_id": "05433fc9-a0fd-5105-a0bf-222b56ccdaee",
        "query_name": "q05",
        "read_bytes": 1323160,
        "read_rows": 131072,
        "real_time_us": 98856,
        "result_rows": 48,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976458456142,
        "synchronous_read_wait_us": 3295,
        "system_time_us": 29839,
        "user_time_us": 2144
      },
      {
        "disk_read_elapsed_us": 1760,
        "elapsed_seconds": 0.003,
        "file_descriptor_read_bytes": 476895,
        "finished_at_unix_us": 1785976458811013,
        "gating": true,
        "os_cpu_virtual_time_us": 6590,
        "os_cpu_wait_time_us": 182,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 476895,
        "page_cache_miss_elapsed_us": 1752,
        "peak_memory_bytes": 541088,
        "query_class": "one_hop",
        "query_id": "4d1ec754-13eb-50d6-a22c-98ed007e69a9",
        "query_name": "q05",
        "read_bytes": 920776,
        "read_rows": 65536,
        "real_time_us": 21612,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976458807747,
        "synchronous_read_wait_us": 3266,
        "system_time_us": 2263,
        "user_time_us": 4343
      },
      {
        "disk_read_elapsed_us": 3727,
        "elapsed_seconds": 0.021,
        "file_descriptor_read_bytes": 424939,
        "finished_at_unix_us": 1785976469209114,
        "gating": false,
        "os_cpu_virtual_time_us": 12627,
        "os_cpu_wait_time_us": 1385,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 206600,
        "page_cache_miss_elapsed_us": 2186,
        "peak_memory_bytes": 574712,
        "query_class": "two_hop",
        "query_id": "e3fe4ac0-fa86-5a02-8efd-25c540966369",
        "query_name": "q06",
        "read_bytes": 524288,
        "read_rows": 65536,
        "real_time_us": 467142,
        "result_rows": 1,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976469188230,
        "synchronous_read_wait_us": 120496,
        "system_time_us": 5742,
        "user_time_us": 6955
      },
      {
        "disk_read_elapsed_us": 5130418,
        "elapsed_seconds": 0.448,
        "file_descriptor_read_bytes": 1460024772,
        "finished_at_unix_us": 1785976470016639,
        "gating": false,
        "os_cpu_virtual_time_us": 2090321,
        "os_cpu_wait_time_us": 177813,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1460024772,
        "page_cache_miss_elapsed_us": 5125822,
        "peak_memory_bytes": 15620527,
        "query_class": "two_hop",
        "query_id": "9d2e2953-22dd-5b31-b4e5-9cf8066454f2",
        "query_name": "q06",
        "read_bytes": 3341347016,
        "read_rows": 208852723,
        "real_time_us": 14131244,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976469568589,
        "synchronous_read_wait_us": 6128121,
        "system_time_us": 561135,
        "user_time_us": 1534635
      },
      {
        "disk_read_elapsed_us": 2664072,
        "elapsed_seconds": 0.312,
        "file_descriptor_read_bytes": 1460826914,
        "finished_at_unix_us": 1785976470673192,
        "gating": false,
        "os_cpu_virtual_time_us": 2252379,
        "os_cpu_wait_time_us": 299495,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1460826914,
        "page_cache_miss_elapsed_us": 2656574,
        "peak_memory_bytes": 22173063,
        "query_class": "two_hop",
        "query_id": "31906d93-f6aa-506e-9e0d-98386489f28e",
        "query_name": "q06",
        "read_bytes": 3341515768,
        "read_rows": 208852723,
        "real_time_us": 8949940,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976470361046,
        "synchronous_read_wait_us": 3801928,
        "system_time_us": 631537,
        "user_time_us": 1625826
      },
      {
        "disk_read_elapsed_us": 438,
        "elapsed_seconds": 0.004,
        "file_descriptor_read_bytes": 147166,
        "finished_at_unix_us": 1785976471038744,
        "gating": false,
        "os_cpu_virtual_time_us": 12603,
        "os_cpu_wait_time_us": 84,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 147166,
        "page_cache_miss_elapsed_us": 433,
        "peak_memory_bytes": 540480,
        "query_class": "two_hop",
        "query_id": "8be06a02-9757-5ba0-b974-acaa423bac3f",
        "query_name": "q06",
        "read_bytes": 524288,
        "read_rows": 65536,
        "real_time_us": 53632,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976471034052,
        "synchronous_read_wait_us": 914,
        "system_time_us": 9879,
        "user_time_us": 2748
      },
      {
        "disk_read_elapsed_us": 2710788,
        "elapsed_seconds": 0.307,
        "file_descriptor_read_bytes": 1460035758,
        "finished_at_unix_us": 1785976471714769,
        "gating": false,
        "os_cpu_virtual_time_us": 2165835,
        "os_cpu_wait_time_us": 299875,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1460035758,
        "page_cache_miss_elapsed_us": 2704877,
        "peak_memory_bytes": 14939938,
        "query_class": "two_hop",
        "query_id": "ca252312-d31a-51f9-97b5-8e8957b9d0f9",
        "query_name": "q06",
        "read_bytes": 3341347016,
        "read_rows": 208852723,
        "real_time_us": 8899066,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976471407789,
        "synchronous_read_wait_us": 3835444,
        "system_time_us": 594106,
        "user_time_us": 1576654
      },
      {
        "disk_read_elapsed_us": 2745127,
        "elapsed_seconds": 0.32,
        "file_descriptor_read_bytes": 1460110614,
        "finished_at_unix_us": 1785976472413434,
        "gating": false,
        "os_cpu_virtual_time_us": 2288377,
        "os_cpu_wait_time_us": 346222,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1460110614,
        "page_cache_miss_elapsed_us": 2738900,
        "peak_memory_bytes": 20584611,
        "query_class": "two_hop",
        "query_id": "06e16dca-0cb0-5a21-a590-9ab54e9aecf3",
        "query_name": "q06",
        "read_bytes": 3341515768,
        "read_rows": 208852723,
        "real_time_us": 9207989,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976472092868,
        "synchronous_read_wait_us": 3935934,
        "system_time_us": 617887,
        "user_time_us": 1675682
      },
      {
        "disk_read_elapsed_us": 3070196,
        "elapsed_seconds": 3.876,
        "file_descriptor_read_bytes": 2696642121,
        "finished_at_unix_us": 1785976485439148,
        "gating": true,
        "os_cpu_virtual_time_us": 56108680,
        "os_cpu_wait_time_us": 2915784,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1294640013,
        "page_cache_miss_elapsed_us": 1196236,
        "peak_memory_bytes": 6512432789,
        "query_class": "routine",
        "query_id": "98beb1b8-f4dc-5c3f-8698-b25017f646c8",
        "query_name": "q07",
        "read_bytes": 2296659057,
        "read_rows": 208787187,
        "real_time_us": 78126755,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976481612682,
        "synchronous_read_wait_us": 3299975,
        "system_time_us": 1799168,
        "user_time_us": 54314499
      },
      {
        "disk_read_elapsed_us": 2432877,
        "elapsed_seconds": 3.774,
        "file_descriptor_read_bytes": 2697050727,
        "finished_at_unix_us": 1785976489584738,
        "gating": true,
        "os_cpu_virtual_time_us": 56558119,
        "os_cpu_wait_time_us": 2141374,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1294292300,
        "page_cache_miss_elapsed_us": 674380,
        "peak_memory_bytes": 5881162338,
        "query_class": "routine",
        "query_id": "8f02c1e1-b7c5-5c70-90de-d5aac44f331b",
        "query_name": "q07",
        "read_bytes": 2296659057,
        "read_rows": 208787187,
        "real_time_us": 75097902,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976485868620,
        "synchronous_read_wait_us": 2356887,
        "system_time_us": 1832096,
        "user_time_us": 54732028
      },
      {
        "disk_read_elapsed_us": 2492881,
        "elapsed_seconds": 3.922,
        "file_descriptor_read_bytes": 2695533017,
        "finished_at_unix_us": 1785976493869540,
        "gating": true,
        "os_cpu_virtual_time_us": 57357337,
        "os_cpu_wait_time_us": 2510587,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1294279020,
        "page_cache_miss_elapsed_us": 792959,
        "peak_memory_bytes": 6029003369,
        "query_class": "routine",
        "query_id": "58755398-ae4b-5258-8d79-71348767369e",
        "query_name": "q07",
        "read_bytes": 2296659057,
        "read_rows": 208787187,
        "real_time_us": 78113390,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976490010295,
        "synchronous_read_wait_us": 2579869,
        "system_time_us": 1825379,
        "user_time_us": 55538292
      },
      {
        "disk_read_elapsed_us": 2689751,
        "elapsed_seconds": 3.895,
        "file_descriptor_read_bytes": 2695751101,
        "finished_at_unix_us": 1785976498141354,
        "gating": true,
        "os_cpu_virtual_time_us": 58426965,
        "os_cpu_wait_time_us": 2399416,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1294370227,
        "page_cache_miss_elapsed_us": 755377,
        "peak_memory_bytes": 5819709087,
        "query_class": "routine",
        "query_id": "ca0b271f-58da-5e7a-ae72-b5fb29797641",
        "query_name": "q07",
        "read_bytes": 2296659057,
        "read_rows": 208787187,
        "real_time_us": 77676181,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976494301633,
        "synchronous_read_wait_us": 2537154,
        "system_time_us": 1918393,
        "user_time_us": 56514617
      },
      {
        "disk_read_elapsed_us": 2756687,
        "elapsed_seconds": 3.961,
        "file_descriptor_read_bytes": 2697132773,
        "finished_at_unix_us": 1785976502419822,
        "gating": true,
        "os_cpu_virtual_time_us": 58887452,
        "os_cpu_wait_time_us": 2425427,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1294947493,
        "page_cache_miss_elapsed_us": 806625,
        "peak_memory_bytes": 5803160613,
        "query_class": "routine",
        "query_id": "590f6f1c-a94f-543d-9cc9-292c8eca5018",
        "query_name": "q07",
        "read_bytes": 2296659057,
        "read_rows": 208787187,
        "real_time_us": 78839183,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976498525742,
        "synchronous_read_wait_us": 2566212,
        "system_time_us": 1976423,
        "user_time_us": 56917095
      },
      {
        "disk_read_elapsed_us": 2670194,
        "elapsed_seconds": 3.99,
        "file_descriptor_read_bytes": 2695239736,
        "finished_at_unix_us": 1785976506773755,
        "gating": true,
        "os_cpu_virtual_time_us": 59512448,
        "os_cpu_wait_time_us": 2346086,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1294527717,
        "page_cache_miss_elapsed_us": 733325,
        "peak_memory_bytes": 6104483685,
        "query_class": "routine",
        "query_id": "37eecc92-ac52-54ae-8794-7f5398c6662d",
        "query_name": "q07",
        "read_bytes": 2296659057,
        "read_rows": 208787187,
        "real_time_us": 79244642,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785976502855922,
        "synchronous_read_wait_us": 2519766,
        "system_time_us": 2121950,
        "user_time_us": 57396899
      }
    ],
    "stage2_medium": [
      {
        "disk_read_elapsed_us": 29314,
        "elapsed_seconds": 0.043,
        "file_descriptor_read_bytes": 10305879,
        "finished_at_unix_us": 1785974648717827,
        "gating": true,
        "os_cpu_virtual_time_us": 235659,
        "os_cpu_wait_time_us": 24040,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10305879,
        "page_cache_miss_elapsed_us": 29056,
        "peak_memory_bytes": 120719844,
        "query_class": "routine",
        "query_id": "df512afc-6dbe-5945-a5d1-e55bf577bf44",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 903170,
        "result_rows": 9810,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974648674962,
        "synchronous_read_wait_us": 139698,
        "system_time_us": 25505,
        "user_time_us": 210363
      },
      {
        "disk_read_elapsed_us": 35080,
        "elapsed_seconds": 0.05,
        "file_descriptor_read_bytes": 10168016,
        "finished_at_unix_us": 1785974649121558,
        "gating": true,
        "os_cpu_virtual_time_us": 226764,
        "os_cpu_wait_time_us": 22802,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10168016,
        "page_cache_miss_elapsed_us": 34877,
        "peak_memory_bytes": 121842048,
        "query_class": "routine",
        "query_id": "daf2a53e-c750-5e2f-860b-e1505cfea366",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 1003284,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974649071426,
        "synchronous_read_wait_us": 79657,
        "system_time_us": 16419,
        "user_time_us": 210553
      },
      {
        "disk_read_elapsed_us": 37846,
        "elapsed_seconds": 0.026,
        "file_descriptor_read_bytes": 10101383,
        "finished_at_unix_us": 1785974649476827,
        "gating": true,
        "os_cpu_virtual_time_us": 227595,
        "os_cpu_wait_time_us": 19036,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10101383,
        "page_cache_miss_elapsed_us": 37622,
        "peak_memory_bytes": 121716007,
        "query_class": "routine",
        "query_id": "d3bb4593-4c92-5135-a170-ffa8c6570ed0",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 529419,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974649450629,
        "synchronous_read_wait_us": 71596,
        "system_time_us": 12670,
        "user_time_us": 215107
      },
      {
        "disk_read_elapsed_us": 36114,
        "elapsed_seconds": 0.026,
        "file_descriptor_read_bytes": 10115050,
        "finished_at_unix_us": 1785974649848518,
        "gating": true,
        "os_cpu_virtual_time_us": 226286,
        "os_cpu_wait_time_us": 19147,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10115050,
        "page_cache_miss_elapsed_us": 35870,
        "peak_memory_bytes": 122200682,
        "query_class": "routine",
        "query_id": "5a32df48-5741-5587-ac89-9ce3aba1a9ab",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 531734,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974649822036,
        "synchronous_read_wait_us": 89568,
        "system_time_us": 16236,
        "user_time_us": 210240
      },
      {
        "disk_read_elapsed_us": 22562,
        "elapsed_seconds": 0.023,
        "file_descriptor_read_bytes": 10112421,
        "finished_at_unix_us": 1785974650221729,
        "gating": true,
        "os_cpu_virtual_time_us": 224548,
        "os_cpu_wait_time_us": 13839,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10112421,
        "page_cache_miss_elapsed_us": 22355,
        "peak_memory_bytes": 122017461,
        "query_class": "routine",
        "query_id": "e04f25c3-0733-5e23-9720-f93eefba728d",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 462864,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974650198093,
        "synchronous_read_wait_us": 72929,
        "system_time_us": 16738,
        "user_time_us": 207973
      },
      {
        "disk_read_elapsed_us": 27886,
        "elapsed_seconds": 0.026,
        "file_descriptor_read_bytes": 10285960,
        "finished_at_unix_us": 1785974650590626,
        "gating": true,
        "os_cpu_virtual_time_us": 230848,
        "os_cpu_wait_time_us": 16817,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10285960,
        "page_cache_miss_elapsed_us": 27687,
        "peak_memory_bytes": 121686702,
        "query_class": "routine",
        "query_id": "3f5f661e-7b16-5e6b-8061-a243b02826cf",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 514605,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974650564656,
        "synchronous_read_wait_us": 90740,
        "system_time_us": 18140,
        "user_time_us": 212902
      },
      {
        "disk_read_elapsed_us": 2347009,
        "elapsed_seconds": 9.431,
        "file_descriptor_read_bytes": 3246065014,
        "finished_at_unix_us": 1785974668685080,
        "gating": true,
        "os_cpu_virtual_time_us": 15220508,
        "os_cpu_wait_time_us": 3172084,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 190170766,
        "page_cache_miss_elapsed_us": 98246,
        "peak_memory_bytes": 2987820754,
        "query_class": "join",
        "query_id": "13595f55-8ce6-5f96-9afd-a4a8889d126a",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 187704039,
        "result_rows": 579800,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974659316374,
        "synchronous_read_wait_us": 489253,
        "system_time_us": 1028073,
        "user_time_us": 14193574
      },
      {
        "disk_read_elapsed_us": 2356096,
        "elapsed_seconds": 9.479,
        "file_descriptor_read_bytes": 3080373107,
        "finished_at_unix_us": 1785974678523105,
        "gating": true,
        "os_cpu_virtual_time_us": 15454940,
        "os_cpu_wait_time_us": 3179491,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 190144830,
        "page_cache_miss_elapsed_us": 102799,
        "peak_memory_bytes": 3015517108,
        "query_class": "join",
        "query_id": "a2848046-3ec2-5022-963e-ecd8f76e25e6",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 188410389,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974669106286,
        "synchronous_read_wait_us": 221103,
        "system_time_us": 1072529,
        "user_time_us": 14383429
      },
      {
        "disk_read_elapsed_us": 2559516,
        "elapsed_seconds": 9.837,
        "file_descriptor_read_bytes": 3176888851,
        "finished_at_unix_us": 1785974688713691,
        "gating": true,
        "os_cpu_virtual_time_us": 15837398,
        "os_cpu_wait_time_us": 3549855,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 190144830,
        "page_cache_miss_elapsed_us": 99063,
        "peak_memory_bytes": 3016957712,
        "query_class": "join",
        "query_id": "5504b261-1dca-5b3c-a586-47a9e9403c20",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 195587507,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974678939785,
        "synchronous_read_wait_us": 211597,
        "system_time_us": 1289986,
        "user_time_us": 14548390
      },
      {
        "disk_read_elapsed_us": 2793742,
        "elapsed_seconds": 10.262,
        "file_descriptor_read_bytes": 3535241458,
        "finished_at_unix_us": 1785974699329582,
        "gating": true,
        "os_cpu_virtual_time_us": 16342673,
        "os_cpu_wait_time_us": 3746146,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 189672193,
        "page_cache_miss_elapsed_us": 109146,
        "peak_memory_bytes": 3037161754,
        "query_class": "join",
        "query_id": "edd03e6a-5f6b-5a3c-9c5b-bc50f3eddaad",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 203976602,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974689131153,
        "synchronous_read_wait_us": 219166,
        "system_time_us": 1409922,
        "user_time_us": 14933743
      },
      {
        "disk_read_elapsed_us": 2576916,
        "elapsed_seconds": 9.79,
        "file_descriptor_read_bytes": 3231609904,
        "finished_at_unix_us": 1785974709456225,
        "gating": true,
        "os_cpu_virtual_time_us": 16084658,
        "os_cpu_wait_time_us": 4204833,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 190144830,
        "page_cache_miss_elapsed_us": 87461,
        "peak_memory_bytes": 3026240779,
        "query_class": "join",
        "query_id": "bfad4687-cb42-5ffe-bbec-e399dc66ffac",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 194413598,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974699740500,
        "synchronous_read_wait_us": 200743,
        "system_time_us": 1304199,
        "user_time_us": 14781505
      },
      {
        "disk_read_elapsed_us": 2556347,
        "elapsed_seconds": 9.903,
        "file_descriptor_read_bytes": 3246963283,
        "finished_at_unix_us": 1785974719721577,
        "gating": true,
        "os_cpu_virtual_time_us": 16043774,
        "os_cpu_wait_time_us": 3152047,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 189833460,
        "page_cache_miss_elapsed_us": 109726,
        "peak_memory_bytes": 3002555520,
        "query_class": "join",
        "query_id": "c63b7a6c-1bb7-5a2d-8f4b-edc4eb13fe71",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 196844577,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974709885307,
        "synchronous_read_wait_us": 225920,
        "system_time_us": 1345187,
        "user_time_us": 14699694
      },
      {
        "disk_read_elapsed_us": 2992274,
        "elapsed_seconds": 2.723,
        "file_descriptor_read_bytes": 3045512439,
        "finished_at_unix_us": 1785974732773134,
        "gating": true,
        "os_cpu_virtual_time_us": 15687546,
        "os_cpu_wait_time_us": 1509007,
        "os_read_bytes": 131072,
        "page_cache_miss_bytes": 2737428583,
        "page_cache_miss_elapsed_us": 2589068,
        "peak_memory_bytes": 4396507532,
        "query_class": "join",
        "query_id": "55a2bf14-7bc6-50bb-b8f8-e7afc7b5a6d8",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 56977581,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974730071788,
        "synchronous_read_wait_us": 6113238,
        "system_time_us": 1329277,
        "user_time_us": 14368746
      },
      {
        "disk_read_elapsed_us": 3027995,
        "elapsed_seconds": 2.953,
        "file_descriptor_read_bytes": 3044322967,
        "finished_at_unix_us": 1785974736209317,
        "gating": true,
        "os_cpu_virtual_time_us": 16055899,
        "os_cpu_wait_time_us": 2153048,
        "os_read_bytes": 32768,
        "page_cache_miss_bytes": 2736417568,
        "page_cache_miss_elapsed_us": 2640797,
        "peak_memory_bytes": 4437483436,
        "query_class": "join",
        "query_id": "68b45e30-86bb-5487-9691-09331c63a648",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 61351883,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974733279442,
        "synchronous_read_wait_us": 5869303,
        "system_time_us": 1452394,
        "user_time_us": 14614187
      },
      {
        "disk_read_elapsed_us": 3176450,
        "elapsed_seconds": 2.989,
        "file_descriptor_read_bytes": 3044386924,
        "finished_at_unix_us": 1785974739688344,
        "gating": true,
        "os_cpu_virtual_time_us": 16090851,
        "os_cpu_wait_time_us": 1450303,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2736474530,
        "page_cache_miss_elapsed_us": 2768179,
        "peak_memory_bytes": 4360479483,
        "query_class": "join",
        "query_id": "c3ea97aa-7c10-5851-805d-648e39c76f4d",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 62242803,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974736722351,
        "synchronous_read_wait_us": 6014434,
        "system_time_us": 1475299,
        "user_time_us": 14625569
      },
      {
        "disk_read_elapsed_us": 3108386,
        "elapsed_seconds": 2.924,
        "file_descriptor_read_bytes": 3045720994,
        "finished_at_unix_us": 1785974743091827,
        "gating": true,
        "os_cpu_virtual_time_us": 15818416,
        "os_cpu_wait_time_us": 1584145,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2737678626,
        "page_cache_miss_elapsed_us": 2714692,
        "peak_memory_bytes": 4371372899,
        "query_class": "join",
        "query_id": "02ca305d-ad37-5cb1-a79a-a037ed6dc1df",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 60732657,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974740191706,
        "synchronous_read_wait_us": 5885406,
        "system_time_us": 1438563,
        "user_time_us": 14390189
      },
      {
        "disk_read_elapsed_us": 3264280,
        "elapsed_seconds": 3.017,
        "file_descriptor_read_bytes": 3046321909,
        "finished_at_unix_us": 1785974746583635,
        "gating": true,
        "os_cpu_virtual_time_us": 16071965,
        "os_cpu_wait_time_us": 1495076,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2738333986,
        "page_cache_miss_elapsed_us": 2862540,
        "peak_memory_bytes": 4439234373,
        "query_class": "join",
        "query_id": "5e44ed1a-1a6c-53c4-963f-15b1773e443c",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 62903572,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974743589346,
        "synchronous_read_wait_us": 6164654,
        "system_time_us": 1578359,
        "user_time_us": 14503935
      },
      {
        "disk_read_elapsed_us": 3162582,
        "elapsed_seconds": 2.943,
        "file_descriptor_read_bytes": 3044084743,
        "finished_at_unix_us": 1785974749975078,
        "gating": true,
        "os_cpu_virtual_time_us": 16145052,
        "os_cpu_wait_time_us": 1559170,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2736081314,
        "page_cache_miss_elapsed_us": 2758518,
        "peak_memory_bytes": 4402891518,
        "query_class": "join",
        "query_id": "940ad897-60ba-5c49-9760-e4c1df1d7253",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 61331983,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974747054076,
        "synchronous_read_wait_us": 6286640,
        "system_time_us": 1640795,
        "user_time_us": 14512673
      },
      {
        "disk_read_elapsed_us": 93551,
        "elapsed_seconds": 2.504,
        "file_descriptor_read_bytes": 137516573,
        "finished_at_unix_us": 1785974763235925,
        "gating": true,
        "os_cpu_virtual_time_us": 5075910,
        "os_cpu_wait_time_us": 21226,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137516573,
        "page_cache_miss_elapsed_us": 92502,
        "peak_memory_bytes": 2268927312,
        "query_class": "join",
        "query_id": "7ba2143e-1129-5b61-aa62-5815d203c396",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 50274578,
        "result_rows": 110456,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974760731883,
        "synchronous_read_wait_us": 359503,
        "system_time_us": 75069,
        "user_time_us": 5001751
      },
      {
        "disk_read_elapsed_us": 90411,
        "elapsed_seconds": 2.44,
        "file_descriptor_read_bytes": 137050417,
        "finished_at_unix_us": 1785974766046458,
        "gating": true,
        "os_cpu_virtual_time_us": 5030319,
        "os_cpu_wait_time_us": 21023,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137050417,
        "page_cache_miss_elapsed_us": 89442,
        "peak_memory_bytes": 2275007287,
        "query_class": "join",
        "query_id": "cedb075c-63d5-5b0e-95b3-395ba6ca4d9a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 48767129,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974763607007,
        "synchronous_read_wait_us": 188913,
        "system_time_us": 68485,
        "user_time_us": 4962736
      },
      {
        "disk_read_elapsed_us": 106666,
        "elapsed_seconds": 2.512,
        "file_descriptor_read_bytes": 136915107,
        "finished_at_unix_us": 1785974768903109,
        "gating": true,
        "os_cpu_virtual_time_us": 5098029,
        "os_cpu_wait_time_us": 13392,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 136915107,
        "page_cache_miss_elapsed_us": 105761,
        "peak_memory_bytes": 2265741242,
        "query_class": "join",
        "query_id": "9801aa14-b9e6-5fd2-b51f-036a8ddf9c9a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 50268334,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974766391930,
        "synchronous_read_wait_us": 197444,
        "system_time_us": 64083,
        "user_time_us": 5034776
      },
      {
        "disk_read_elapsed_us": 102184,
        "elapsed_seconds": 2.502,
        "file_descriptor_read_bytes": 136876467,
        "finished_at_unix_us": 1785974771743661,
        "gating": true,
        "os_cpu_virtual_time_us": 5077983,
        "os_cpu_wait_time_us": 17933,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 136876467,
        "page_cache_miss_elapsed_us": 101247,
        "peak_memory_bytes": 2252808475,
        "query_class": "join",
        "query_id": "cac9576c-5bbd-5797-b028-2d781cf4f7c1",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 50061000,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974769242253,
        "synchronous_read_wait_us": 190342,
        "system_time_us": 47922,
        "user_time_us": 5030920
      },
      {
        "disk_read_elapsed_us": 99818,
        "elapsed_seconds": 2.48,
        "file_descriptor_read_bytes": 137176760,
        "finished_at_unix_us": 1785974774579601,
        "gating": true,
        "os_cpu_virtual_time_us": 5119097,
        "os_cpu_wait_time_us": 11688,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137176760,
        "page_cache_miss_elapsed_us": 98878,
        "peak_memory_bytes": 2276506270,
        "query_class": "join",
        "query_id": "0810c65e-2c98-5cd1-b43c-bfb4c95a789a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 49614107,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974772100560,
        "synchronous_read_wait_us": 190026,
        "system_time_us": 67842,
        "user_time_us": 5052144
      },
      {
        "disk_read_elapsed_us": 109583,
        "elapsed_seconds": 2.5,
        "file_descriptor_read_bytes": 137364333,
        "finished_at_unix_us": 1785974777442047,
        "gating": true,
        "os_cpu_virtual_time_us": 5089403,
        "os_cpu_wait_time_us": 17878,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137364333,
        "page_cache_miss_elapsed_us": 108533,
        "peak_memory_bytes": 2263372477,
        "query_class": "join",
        "query_id": "3b30e5aa-2e1a-5868-8c48-f7db737325cd",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 50022946,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974774942629,
        "synchronous_read_wait_us": 200824,
        "system_time_us": 71690,
        "user_time_us": 5018606
      },
      {
        "disk_read_elapsed_us": 830681,
        "elapsed_seconds": 0.102,
        "file_descriptor_read_bytes": 413398559,
        "finished_at_unix_us": 1785974786516727,
        "gating": true,
        "os_cpu_virtual_time_us": 487436,
        "os_cpu_wait_time_us": 72081,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 413324749,
        "page_cache_miss_elapsed_us": 828521,
        "peak_memory_bytes": 2202080,
        "query_class": "one_hop",
        "query_id": "b730b9c4-9614-57b4-b429-efae8d8cca95",
        "query_name": "q05",
        "read_bytes": 563458944,
        "read_rows": 70432368,
        "real_time_us": 3156217,
        "result_rows": 0,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974786414371,
        "synchronous_read_wait_us": 1475701,
        "system_time_us": 180344,
        "user_time_us": 308561
      },
      {
        "disk_read_elapsed_us": 801426,
        "elapsed_seconds": 0.086,
        "file_descriptor_read_bytes": 413607548,
        "finished_at_unix_us": 1785974786969697,
        "gating": true,
        "os_cpu_virtual_time_us": 491220,
        "os_cpu_wait_time_us": 70550,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 413607548,
        "page_cache_miss_elapsed_us": 799955,
        "peak_memory_bytes": 2169750,
        "query_class": "one_hop",
        "query_id": "4c447197-0298-5dcc-863c-bb68268e94b7",
        "query_name": "q05",
        "read_bytes": 563555752,
        "read_rows": 70432368,
        "real_time_us": 2501545,
        "result_rows": 46,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974786883056,
        "synchronous_read_wait_us": 1118225,
        "system_time_us": 178495,
        "user_time_us": 314342
      },
      {
        "disk_read_elapsed_us": 840687,
        "elapsed_seconds": 0.088,
        "file_descriptor_read_bytes": 414019655,
        "finished_at_unix_us": 1785974787406584,
        "gating": true,
        "os_cpu_virtual_time_us": 487060,
        "os_cpu_wait_time_us": 79349,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 414019655,
        "page_cache_miss_elapsed_us": 837266,
        "peak_memory_bytes": 2253126,
        "query_class": "one_hop",
        "query_id": "cecc163f-7a64-5b1a-8a6b-67432d383cf3",
        "query_name": "q05",
        "read_bytes": 563590016,
        "read_rows": 70432368,
        "real_time_us": 2571020,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974787318560,
        "synchronous_read_wait_us": 1160341,
        "system_time_us": 188233,
        "user_time_us": 300381
      },
      {
        "disk_read_elapsed_us": 0,
        "elapsed_seconds": 0.001,
        "file_descriptor_read_bytes": 0,
        "finished_at_unix_us": 1785974787764785,
        "gating": true,
        "os_cpu_virtual_time_us": 1085,
        "os_cpu_wait_time_us": 0,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 0,
        "page_cache_miss_elapsed_us": 0,
        "peak_memory_bytes": 317792,
        "query_class": "one_hop",
        "query_id": "56847c14-8888-5648-b76e-e6bcc1efb0fe",
        "query_name": "q05",
        "read_bytes": 0,
        "read_rows": 0,
        "real_time_us": 1398,
        "result_rows": 0,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974787763644,
        "synchronous_read_wait_us": 0,
        "system_time_us": 69,
        "user_time_us": 1017
      },
      {
        "disk_read_elapsed_us": 213,
        "elapsed_seconds": 0.006,
        "file_descriptor_read_bytes": 105210,
        "finished_at_unix_us": 1785974788117070,
        "gating": true,
        "os_cpu_virtual_time_us": 10562,
        "os_cpu_wait_time_us": 6,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 105210,
        "page_cache_miss_elapsed_us": 210,
        "peak_memory_bytes": 355542,
        "query_class": "one_hop",
        "query_id": "05433fc9-a0fd-5105-a0bf-222b56ccdaee",
        "query_name": "q05",
        "read_bytes": 227880,
        "read_rows": 16384,
        "real_time_us": 28767,
        "result_rows": 46,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974788110348,
        "synchronous_read_wait_us": 441,
        "system_time_us": 8755,
        "user_time_us": 1812
      },
      {
        "disk_read_elapsed_us": 230,
        "elapsed_seconds": 0.002,
        "file_descriptor_read_bytes": 84248,
        "finished_at_unix_us": 1785974788448338,
        "gating": true,
        "os_cpu_virtual_time_us": 2205,
        "os_cpu_wait_time_us": 21,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 84248,
        "page_cache_miss_elapsed_us": 228,
        "peak_memory_bytes": 435830,
        "query_class": "one_hop",
        "query_id": "4d1ec754-13eb-50d6-a22c-98ed007e69a9",
        "query_name": "q05",
        "read_bytes": 262144,
        "read_rows": 16384,
        "real_time_us": 6451,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974788446071,
        "synchronous_read_wait_us": 453,
        "system_time_us": 604,
        "user_time_us": 1610
      },
      {
        "disk_read_elapsed_us": 3957,
        "elapsed_seconds": 0.009,
        "file_descriptor_read_bytes": 101569,
        "finished_at_unix_us": 1785974798221112,
        "gating": false,
        "os_cpu_virtual_time_us": 6096,
        "os_cpu_wait_time_us": 51,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 27759,
        "page_cache_miss_elapsed_us": 1896,
        "peak_memory_bytes": 519840,
        "query_class": "two_hop",
        "query_id": "e3fe4ac0-fa86-5a02-8efd-25c540966369",
        "query_name": "q06",
        "read_bytes": 131072,
        "read_rows": 16384,
        "real_time_us": 100158,
        "result_rows": 1,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974798211703,
        "synchronous_read_wait_us": 2312,
        "system_time_us": 2847,
        "user_time_us": 3262
      },
      {
        "disk_read_elapsed_us": 789253,
        "elapsed_seconds": 0.094,
        "file_descriptor_read_bytes": 453110220,
        "finished_at_unix_us": 1785974798677560,
        "gating": false,
        "os_cpu_virtual_time_us": 659667,
        "os_cpu_wait_time_us": 107887,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 453110220,
        "page_cache_miss_elapsed_us": 787175,
        "peak_memory_bytes": 6051470,
        "query_class": "two_hop",
        "query_id": "9d2e2953-22dd-5b31-b4e5-9cf8066454f2",
        "query_name": "q06",
        "read_bytes": 1126883624,
        "read_rows": 70432368,
        "real_time_us": 2672512,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974798583121,
        "synchronous_read_wait_us": 1183750,
        "system_time_us": 209554,
        "user_time_us": 451755
      },
      {
        "disk_read_elapsed_us": 755244,
        "elapsed_seconds": 0.102,
        "file_descriptor_read_bytes": 452127313,
        "finished_at_unix_us": 1785974799133949,
        "gating": false,
        "os_cpu_virtual_time_us": 708368,
        "os_cpu_wait_time_us": 142943,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 452127313,
        "page_cache_miss_elapsed_us": 752678,
        "peak_memory_bytes": 13293576,
        "query_class": "two_hop",
        "query_id": "31906d93-f6aa-506e-9e0d-98386489f28e",
        "query_name": "q06",
        "read_bytes": 1126917888,
        "read_rows": 70432368,
        "real_time_us": 2786169,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974799031447,
        "synchronous_read_wait_us": 1171865,
        "system_time_us": 203444,
        "user_time_us": 506409
      },
      {
        "disk_read_elapsed_us": 114,
        "elapsed_seconds": 0.003,
        "file_descriptor_read_bytes": 8850,
        "finished_at_unix_us": 1785974799478852,
        "gating": false,
        "os_cpu_virtual_time_us": 5210,
        "os_cpu_wait_time_us": 17,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 8850,
        "page_cache_miss_elapsed_us": 112,
        "peak_memory_bytes": 500672,
        "query_class": "two_hop",
        "query_id": "8be06a02-9757-5ba0-b974-acaa423bac3f",
        "query_name": "q06",
        "read_bytes": 131072,
        "read_rows": 16384,
        "real_time_us": 30404,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974799475391,
        "synchronous_read_wait_us": 223,
        "system_time_us": 3887,
        "user_time_us": 1333
      },
      {
        "disk_read_elapsed_us": 915766,
        "elapsed_seconds": 0.105,
        "file_descriptor_read_bytes": 453253141,
        "finished_at_unix_us": 1785974799933170,
        "gating": false,
        "os_cpu_virtual_time_us": 662349,
        "os_cpu_wait_time_us": 102424,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 453253141,
        "page_cache_miss_elapsed_us": 914114,
        "peak_memory_bytes": 5784438,
        "query_class": "two_hop",
        "query_id": "ca252312-d31a-51f9-97b5-8e8957b9d0f9",
        "query_name": "q06",
        "read_bytes": 1126883624,
        "read_rows": 70432368,
        "real_time_us": 2990331,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974799828211,
        "synchronous_read_wait_us": 1287146,
        "system_time_us": 202839,
        "user_time_us": 461093
      },
      {
        "disk_read_elapsed_us": 773648,
        "elapsed_seconds": 0.101,
        "file_descriptor_read_bytes": 452797797,
        "finished_at_unix_us": 1785974800388821,
        "gating": false,
        "os_cpu_virtual_time_us": 714876,
        "os_cpu_wait_time_us": 113356,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 452797797,
        "page_cache_miss_elapsed_us": 770909,
        "peak_memory_bytes": 13489583,
        "query_class": "two_hop",
        "query_id": "06e16dca-0cb0-5a21-a590-9ab54e9aecf3",
        "query_name": "q06",
        "read_bytes": 1126917888,
        "read_rows": 70432368,
        "real_time_us": 2740085,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974800287650,
        "synchronous_read_wait_us": 1167172,
        "system_time_us": 192405,
        "user_time_us": 524039
      },
      {
        "disk_read_elapsed_us": 838108,
        "elapsed_seconds": 1.212,
        "file_descriptor_read_bytes": 902978594,
        "finished_at_unix_us": 1785974812084820,
        "gating": true,
        "os_cpu_virtual_time_us": 17119788,
        "os_cpu_wait_time_us": 1016274,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 427333306,
        "page_cache_miss_elapsed_us": 272084,
        "peak_memory_bytes": 6583463772,
        "query_class": "routine",
        "query_id": "98beb1b8-f4dc-5c3f-8698-b25017f646c8",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24280646,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974810892398,
        "synchronous_read_wait_us": 1200687,
        "system_time_us": 614870,
        "user_time_us": 16507054
      },
      {
        "disk_read_elapsed_us": 849635,
        "elapsed_seconds": 1.21,
        "file_descriptor_read_bytes": 901764319,
        "finished_at_unix_us": 1785974813677217,
        "gating": true,
        "os_cpu_virtual_time_us": 16719404,
        "os_cpu_wait_time_us": 965484,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426954005,
        "page_cache_miss_elapsed_us": 335569,
        "peak_memory_bytes": 6237256002,
        "query_class": "routine",
        "query_id": "8f02c1e1-b7c5-5c70-90de-d5aac44f331b",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24174902,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974812484759,
        "synchronous_read_wait_us": 1148710,
        "system_time_us": 523529,
        "user_time_us": 16197975
      },
      {
        "disk_read_elapsed_us": 857444,
        "elapsed_seconds": 1.216,
        "file_descriptor_read_bytes": 901520986,
        "finished_at_unix_us": 1785974815252599,
        "gating": true,
        "os_cpu_virtual_time_us": 16869624,
        "os_cpu_wait_time_us": 977270,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 427088751,
        "page_cache_miss_elapsed_us": 272373,
        "peak_memory_bytes": 6423787860,
        "query_class": "routine",
        "query_id": "58755398-ae4b-5258-8d79-71348767369e",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24217243,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974814056605,
        "synchronous_read_wait_us": 892790,
        "system_time_us": 512209,
        "user_time_us": 16359467
      },
      {
        "disk_read_elapsed_us": 887804,
        "elapsed_seconds": 1.231,
        "file_descriptor_read_bytes": 901771725,
        "finished_at_unix_us": 1785974816825805,
        "gating": true,
        "os_cpu_virtual_time_us": 17217098,
        "os_cpu_wait_time_us": 908432,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426736237,
        "page_cache_miss_elapsed_us": 333985,
        "peak_memory_bytes": 5944446716,
        "query_class": "routine",
        "query_id": "ca0b271f-58da-5e7a-ae72-b5fb29797641",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24171519,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974815636447,
        "synchronous_read_wait_us": 1163318,
        "system_time_us": 606784,
        "user_time_us": 16612467
      },
      {
        "disk_read_elapsed_us": 860968,
        "elapsed_seconds": 1.185,
        "file_descriptor_read_bytes": 903013918,
        "finished_at_unix_us": 1785974818383402,
        "gating": true,
        "os_cpu_virtual_time_us": 16996673,
        "os_cpu_wait_time_us": 763682,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 427134898,
        "page_cache_miss_elapsed_us": 322090,
        "peak_memory_bytes": 5549371596,
        "query_class": "routine",
        "query_id": "590f6f1c-a94f-543d-9cc9-292c8eca5018",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 23717916,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974817214614,
        "synchronous_read_wait_us": 957853,
        "system_time_us": 591461,
        "user_time_us": 16407237
      },
      {
        "disk_read_elapsed_us": 827487,
        "elapsed_seconds": 1.418,
        "file_descriptor_read_bytes": 902072150,
        "finished_at_unix_us": 1785974820153456,
        "gating": true,
        "os_cpu_virtual_time_us": 16928360,
        "os_cpu_wait_time_us": 927845,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426929135,
        "page_cache_miss_elapsed_us": 319952,
        "peak_memory_bytes": 5917421348,
        "query_class": "routine",
        "query_id": "37eecc92-ac52-54ae-8794-7f5398c6662d",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 28143930,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974818764258,
        "synchronous_read_wait_us": 1010044,
        "system_time_us": 627577,
        "user_time_us": 16302985
      }
    ],
    "stage2_small": [
      {
        "disk_read_elapsed_us": 7368,
        "elapsed_seconds": 0.035,
        "file_descriptor_read_bytes": 1484311,
        "finished_at_unix_us": 1785974313717186,
        "gating": true,
        "os_cpu_virtual_time_us": 70259,
        "os_cpu_wait_time_us": 306,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1484311,
        "page_cache_miss_elapsed_us": 7336,
        "peak_memory_bytes": 67104249,
        "query_class": "routine",
        "query_id": "df512afc-6dbe-5945-a5d1-e55bf577bf44",
        "query_name": "q01",
        "read_bytes": 12017892,
        "read_rows": 2002982,
        "real_time_us": 872865,
        "result_rows": 6174,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974313682149,
        "synchronous_read_wait_us": 216991,
        "system_time_us": 16592,
        "user_time_us": 53761
      },
      {
        "disk_read_elapsed_us": 4847,
        "elapsed_seconds": 0.011,
        "file_descriptor_read_bytes": 1481768,
        "finished_at_unix_us": 1785974314121203,
        "gating": true,
        "os_cpu_virtual_time_us": 60740,
        "os_cpu_wait_time_us": 244,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1481768,
        "page_cache_miss_elapsed_us": 4791,
        "peak_memory_bytes": 67068817,
        "query_class": "routine",
        "query_id": "daf2a53e-c750-5e2f-860b-e1505cfea366",
        "query_name": "q01",
        "read_bytes": 12017892,
        "read_rows": 2002982,
        "real_time_us": 197073,
        "result_rows": 6174,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974314110061,
        "synchronous_read_wait_us": 10391,
        "system_time_us": 5316,
        "user_time_us": 55461
      },
      {
        "disk_read_elapsed_us": 9090,
        "elapsed_seconds": 0.012,
        "file_descriptor_read_bytes": 1481768,
        "finished_at_unix_us": 1785974314504495,
        "gating": true,
        "os_cpu_virtual_time_us": 63148,
        "os_cpu_wait_time_us": 1702,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1481768,
        "page_cache_miss_elapsed_us": 9059,
        "peak_memory_bytes": 67068817,
        "query_class": "routine",
        "query_id": "d3bb4593-4c92-5135-a170-ffa8c6570ed0",
        "query_name": "q01",
        "read_bytes": 12017892,
        "read_rows": 2002982,
        "real_time_us": 215118,
        "result_rows": 6174,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974314492639,
        "synchronous_read_wait_us": 14533,
        "system_time_us": 12093,
        "user_time_us": 51097
      },
      {
        "disk_read_elapsed_us": 5719,
        "elapsed_seconds": 0.011,
        "file_descriptor_read_bytes": 1481768,
        "finished_at_unix_us": 1785974314848112,
        "gating": true,
        "os_cpu_virtual_time_us": 60557,
        "os_cpu_wait_time_us": 108,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1481768,
        "page_cache_miss_elapsed_us": 5675,
        "peak_memory_bytes": 67068497,
        "query_class": "routine",
        "query_id": "5a32df48-5741-5587-ac89-9ce3aba1a9ab",
        "query_name": "q01",
        "read_bytes": 12017892,
        "read_rows": 2002982,
        "real_time_us": 199578,
        "result_rows": 6174,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974314836869,
        "synchronous_read_wait_us": 11522,
        "system_time_us": 9954,
        "user_time_us": 50649
      },
      {
        "disk_read_elapsed_us": 5839,
        "elapsed_seconds": 0.012,
        "file_descriptor_read_bytes": 1481768,
        "finished_at_unix_us": 1785974315192322,
        "gating": true,
        "os_cpu_virtual_time_us": 63320,
        "os_cpu_wait_time_us": 470,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1481768,
        "page_cache_miss_elapsed_us": 5818,
        "peak_memory_bytes": 67067985,
        "query_class": "routine",
        "query_id": "e04f25c3-0733-5e23-9720-f93eefba728d",
        "query_name": "q01",
        "read_bytes": 12017892,
        "read_rows": 2002982,
        "real_time_us": 224693,
        "result_rows": 6174,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974315179806,
        "synchronous_read_wait_us": 12935,
        "system_time_us": 3762,
        "user_time_us": 59602
      },
      {
        "disk_read_elapsed_us": 6805,
        "elapsed_seconds": 0.013,
        "file_descriptor_read_bytes": 1481768,
        "finished_at_unix_us": 1785974315548476,
        "gating": true,
        "os_cpu_virtual_time_us": 63952,
        "os_cpu_wait_time_us": 1163,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 1481768,
        "page_cache_miss_elapsed_us": 6782,
        "peak_memory_bytes": 67067713,
        "query_class": "routine",
        "query_id": "3f5f661e-7b16-5e6b-8061-a243b02826cf",
        "query_name": "q01",
        "read_bytes": 12017892,
        "read_rows": 2002982,
        "real_time_us": 244403,
        "result_rows": 6174,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974315535077,
        "synchronous_read_wait_us": 12659,
        "system_time_us": 13574,
        "user_time_us": 50408
      },
      {
        "disk_read_elapsed_us": 36252,
        "elapsed_seconds": 0.279,
        "file_descriptor_read_bytes": 38869598,
        "finished_at_unix_us": 1785974326132882,
        "gating": true,
        "os_cpu_virtual_time_us": 1089223,
        "os_cpu_wait_time_us": 8552,
        "os_read_bytes": 126976,
        "page_cache_miss_bytes": 38869598,
        "page_cache_miss_elapsed_us": 36003,
        "peak_memory_bytes": 1148407433,
        "query_class": "join",
        "query_id": "13595f55-8ce6-5f96-9afd-a4a8889d126a",
        "query_name": "q02",
        "read_bytes": 96483111,
        "read_rows": 6146611,
        "real_time_us": 5781353,
        "result_rows": 346801,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974325854110,
        "synchronous_read_wait_us": 445181,
        "system_time_us": 37108,
        "user_time_us": 1052390
      },
      {
        "disk_read_elapsed_us": 44587,
        "elapsed_seconds": 0.242,
        "file_descriptor_read_bytes": 38863703,
        "finished_at_unix_us": 1785974326716502,
        "gating": true,
        "os_cpu_virtual_time_us": 1067609,
        "os_cpu_wait_time_us": 4941,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 38863703,
        "page_cache_miss_elapsed_us": 44234,
        "peak_memory_bytes": 1127852852,
        "query_class": "join",
        "query_id": "a2848046-3ec2-5022-963e-ecd8f76e25e6",
        "query_name": "q02",
        "read_bytes": 96483111,
        "read_rows": 6146611,
        "real_time_us": 4795424,
        "result_rows": 346801,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974326474174,
        "synchronous_read_wait_us": 75740,
        "system_time_us": 15865,
        "user_time_us": 1051961
      },
      {
        "disk_read_elapsed_us": 41672,
        "elapsed_seconds": 0.24,
        "file_descriptor_read_bytes": 38863703,
        "finished_at_unix_us": 1785974327321558,
        "gating": true,
        "os_cpu_virtual_time_us": 1075018,
        "os_cpu_wait_time_us": 15801,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 38863703,
        "page_cache_miss_elapsed_us": 41437,
        "peak_memory_bytes": 1135044912,
        "query_class": "join",
        "query_id": "5504b261-1dca-5b3c-a586-47a9e9403c20",
        "query_name": "q02",
        "read_bytes": 96483111,
        "read_rows": 6146611,
        "real_time_us": 4779269,
        "result_rows": 346801,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974327081505,
        "synchronous_read_wait_us": 70804,
        "system_time_us": 16534,
        "user_time_us": 1058756
      },
      {
        "disk_read_elapsed_us": 43981,
        "elapsed_seconds": 0.245,
        "file_descriptor_read_bytes": 38863703,
        "finished_at_unix_us": 1785974327930240,
        "gating": true,
        "os_cpu_virtual_time_us": 1066068,
        "os_cpu_wait_time_us": 5084,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 38863703,
        "page_cache_miss_elapsed_us": 43761,
        "peak_memory_bytes": 1154349893,
        "query_class": "join",
        "query_id": "edd03e6a-5f6b-5a3c-9c5b-bc50f3eddaad",
        "query_name": "q02",
        "read_bytes": 96483111,
        "read_rows": 6146611,
        "real_time_us": 4772188,
        "result_rows": 346801,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974327685599,
        "synchronous_read_wait_us": 71422,
        "system_time_us": 25095,
        "user_time_us": 1041152
      },
      {
        "disk_read_elapsed_us": 47297,
        "elapsed_seconds": 0.241,
        "file_descriptor_read_bytes": 38863703,
        "finished_at_unix_us": 1785974328541311,
        "gating": true,
        "os_cpu_virtual_time_us": 1046403,
        "os_cpu_wait_time_us": 11987,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 38863703,
        "page_cache_miss_elapsed_us": 47064,
        "peak_memory_bytes": 1152090881,
        "query_class": "join",
        "query_id": "bfad4687-cb42-5ffe-bbec-e399dc66ffac",
        "query_name": "q02",
        "read_bytes": 96483111,
        "read_rows": 6146611,
        "real_time_us": 4807057,
        "result_rows": 346801,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974328299945,
        "synchronous_read_wait_us": 97694,
        "system_time_us": 20887,
        "user_time_us": 1025655
      },
      {
        "disk_read_elapsed_us": 42301,
        "elapsed_seconds": 0.241,
        "file_descriptor_read_bytes": 38863703,
        "finished_at_unix_us": 1785974329120349,
        "gating": true,
        "os_cpu_virtual_time_us": 1059754,
        "os_cpu_wait_time_us": 12066,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 38863703,
        "page_cache_miss_elapsed_us": 42060,
        "peak_memory_bytes": 1127428854,
        "query_class": "join",
        "query_id": "c63b7a6c-1bb7-5a2d-8f4b-edc4eb13fe71",
        "query_name": "q02",
        "read_bytes": 96483111,
        "read_rows": 6146611,
        "real_time_us": 4802770,
        "result_rows": 346801,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974328879504,
        "synchronous_read_wait_us": 76340,
        "system_time_us": 28104,
        "user_time_us": 1031865
      },
      {
        "disk_read_elapsed_us": 3907063,
        "elapsed_seconds": 0.809,
        "file_descriptor_read_bytes": 2569663058,
        "finished_at_unix_us": 1785974341796185,
        "gating": true,
        "os_cpu_virtual_time_us": 6121413,
        "os_cpu_wait_time_us": 1017052,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2569663058,
        "page_cache_miss_elapsed_us": 3888696,
        "peak_memory_bytes": 2401344837,
        "query_class": "join",
        "query_id": "55a2bf14-7bc6-50bb-b8f8-e7afc7b5a6d8",
        "query_name": "q03",
        "read_bytes": 3243457177,
        "read_rows": 124984723,
        "real_time_us": 20373140,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974340987757,
        "synchronous_read_wait_us": 6648006,
        "system_time_us": 1085187,
        "user_time_us": 5045448
      },
      {
        "disk_read_elapsed_us": 3597999,
        "elapsed_seconds": 0.77,
        "file_descriptor_read_bytes": 2570058596,
        "finished_at_unix_us": 1785974342918192,
        "gating": true,
        "os_cpu_virtual_time_us": 6035042,
        "os_cpu_wait_time_us": 984991,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2570058596,
        "page_cache_miss_elapsed_us": 3582350,
        "peak_memory_bytes": 2244996697,
        "query_class": "join",
        "query_id": "68b45e30-86bb-5487-9691-09331c63a648",
        "query_name": "q03",
        "read_bytes": 3243457177,
        "read_rows": 124984723,
        "real_time_us": 19059160,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974342148833,
        "synchronous_read_wait_us": 5985829,
        "system_time_us": 1061176,
        "user_time_us": 4982051
      },
      {
        "disk_read_elapsed_us": 4019154,
        "elapsed_seconds": 0.787,
        "file_descriptor_read_bytes": 2571762532,
        "finished_at_unix_us": 1785974344078842,
        "gating": true,
        "os_cpu_virtual_time_us": 6052356,
        "os_cpu_wait_time_us": 828959,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2571762532,
        "page_cache_miss_elapsed_us": 4003485,
        "peak_memory_bytes": 2244063497,
        "query_class": "join",
        "query_id": "c3ea97aa-7c10-5851-805d-648e39c76f4d",
        "query_name": "q03",
        "read_bytes": 3243457177,
        "read_rows": 124984723,
        "real_time_us": 19868734,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974343292063,
        "synchronous_read_wait_us": 6376142,
        "system_time_us": 1154410,
        "user_time_us": 4906566
      },
      {
        "disk_read_elapsed_us": 3728087,
        "elapsed_seconds": 0.777,
        "file_descriptor_read_bytes": 2570770552,
        "finished_at_unix_us": 1785974345181742,
        "gating": true,
        "os_cpu_virtual_time_us": 6063946,
        "os_cpu_wait_time_us": 932045,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2570770552,
        "page_cache_miss_elapsed_us": 3710674,
        "peak_memory_bytes": 2223398497,
        "query_class": "join",
        "query_id": "02ca305d-ad37-5cb1-a79a-a037ed6dc1df",
        "query_name": "q03",
        "read_bytes": 3243457177,
        "read_rows": 124984723,
        "real_time_us": 19269005,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974344405152,
        "synchronous_read_wait_us": 6088300,
        "system_time_us": 1124665,
        "user_time_us": 4948640
      },
      {
        "disk_read_elapsed_us": 3796935,
        "elapsed_seconds": 0.784,
        "file_descriptor_read_bytes": 2569403236,
        "finished_at_unix_us": 1785974346319665,
        "gating": true,
        "os_cpu_virtual_time_us": 6137821,
        "os_cpu_wait_time_us": 1008458,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2569403236,
        "page_cache_miss_elapsed_us": 3779933,
        "peak_memory_bytes": 2223098545,
        "query_class": "join",
        "query_id": "5e44ed1a-1a6c-53c4-963f-15b1773e443c",
        "query_name": "q03",
        "read_bytes": 3243457177,
        "read_rows": 124984723,
        "real_time_us": 19594189,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974345535493,
        "synchronous_read_wait_us": 6234843,
        "system_time_us": 1180350,
        "user_time_us": 4966528
      },
      {
        "disk_read_elapsed_us": 3750083,
        "elapsed_seconds": 0.797,
        "file_descriptor_read_bytes": 2572024676,
        "finished_at_unix_us": 1785974347466323,
        "gating": true,
        "os_cpu_virtual_time_us": 6245505,
        "os_cpu_wait_time_us": 1066175,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2572024676,
        "page_cache_miss_elapsed_us": 3733460,
        "peak_memory_bytes": 2258253524,
        "query_class": "join",
        "query_id": "940ad897-60ba-5c49-9760-e4c1df1d7253",
        "query_name": "q03",
        "read_bytes": 3243457177,
        "read_rows": 124984723,
        "real_time_us": 19807823,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974346669121,
        "synchronous_read_wait_us": 6318541,
        "system_time_us": 1207826,
        "user_time_us": 5045734
      },
      {
        "disk_read_elapsed_us": 44986,
        "elapsed_seconds": 0.357,
        "file_descriptor_read_bytes": 33122343,
        "finished_at_unix_us": 1785974357580312,
        "gating": true,
        "os_cpu_virtual_time_us": 848479,
        "os_cpu_wait_time_us": 7436,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 33122343,
        "page_cache_miss_elapsed_us": 44756,
        "peak_memory_bytes": 665840762,
        "query_class": "join",
        "query_id": "7ba2143e-1129-5b61-aa62-5815d203c396",
        "query_name": "q04",
        "read_bytes": 111540414,
        "read_rows": 7550998,
        "real_time_us": 7076703,
        "result_rows": 54471,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974357222997,
        "synchronous_read_wait_us": 103179,
        "system_time_us": 35411,
        "user_time_us": 813306
      },
      {
        "disk_read_elapsed_us": 48169,
        "elapsed_seconds": 0.327,
        "file_descriptor_read_bytes": 33117947,
        "finished_at_unix_us": 1785974358245314,
        "gating": true,
        "os_cpu_virtual_time_us": 840176,
        "os_cpu_wait_time_us": 5568,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 33117947,
        "page_cache_miss_elapsed_us": 47641,
        "peak_memory_bytes": 679316734,
        "query_class": "join",
        "query_id": "cedb075c-63d5-5b0e-95b3-395ba6ca4d9a",
        "query_name": "q04",
        "read_bytes": 111540414,
        "read_rows": 7550998,
        "real_time_us": 6444170,
        "result_rows": 54471,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974357918647,
        "synchronous_read_wait_us": 91127,
        "system_time_us": 16805,
        "user_time_us": 823566
      },
      {
        "disk_read_elapsed_us": 40487,
        "elapsed_seconds": 0.33,
        "file_descriptor_read_bytes": 33117947,
        "finished_at_unix_us": 1785974358937965,
        "gating": true,
        "os_cpu_virtual_time_us": 839538,
        "os_cpu_wait_time_us": 11744,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 33117947,
        "page_cache_miss_elapsed_us": 40281,
        "peak_memory_bytes": 679675618,
        "query_class": "join",
        "query_id": "9801aa14-b9e6-5fd2-b51f-036a8ddf9c9a",
        "query_name": "q04",
        "read_bytes": 111540414,
        "read_rows": 7550998,
        "real_time_us": 6552111,
        "result_rows": 54471,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974358608494,
        "synchronous_read_wait_us": 72727,
        "system_time_us": 20943,
        "user_time_us": 818792
      },
      {
        "disk_read_elapsed_us": 31471,
        "elapsed_seconds": 0.324,
        "file_descriptor_read_bytes": 33117947,
        "finished_at_unix_us": 1785974359617409,
        "gating": true,
        "os_cpu_virtual_time_us": 828603,
        "os_cpu_wait_time_us": 10282,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 33117947,
        "page_cache_miss_elapsed_us": 31248,
        "peak_memory_bytes": 666694848,
        "query_class": "join",
        "query_id": "cac9576c-5bbd-5797-b028-2d781cf4f7c1",
        "query_name": "q04",
        "read_bytes": 111540414,
        "read_rows": 7550998,
        "real_time_us": 6396844,
        "result_rows": 54471,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974359293110,
        "synchronous_read_wait_us": 58037,
        "system_time_us": 27916,
        "user_time_us": 800887
      },
      {
        "disk_read_elapsed_us": 52937,
        "elapsed_seconds": 0.344,
        "file_descriptor_read_bytes": 33117947,
        "finished_at_unix_us": 1785974360323696,
        "gating": true,
        "os_cpu_virtual_time_us": 864412,
        "os_cpu_wait_time_us": 24546,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 33117947,
        "page_cache_miss_elapsed_us": 52667,
        "peak_memory_bytes": 681402500,
        "query_class": "join",
        "query_id": "0810c65e-2c98-5cd1-b43c-bfb4c95a789a",
        "query_name": "q04",
        "read_bytes": 111540414,
        "read_rows": 7550998,
        "real_time_us": 6839334,
        "result_rows": 54471,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974359979380,
        "synchronous_read_wait_us": 81812,
        "system_time_us": 27345,
        "user_time_us": 837263
      },
      {
        "disk_read_elapsed_us": 37873,
        "elapsed_seconds": 0.319,
        "file_descriptor_read_bytes": 33117947,
        "finished_at_unix_us": 1785974360982573,
        "gating": true,
        "os_cpu_virtual_time_us": 830807,
        "os_cpu_wait_time_us": 4265,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 33117947,
        "page_cache_miss_elapsed_us": 37687,
        "peak_memory_bytes": 682604838,
        "query_class": "join",
        "query_id": "3b30e5aa-2e1a-5868-8c48-f7db737325cd",
        "query_name": "q04",
        "read_bytes": 111540414,
        "read_rows": 7550998,
        "real_time_us": 6306849,
        "result_rows": 54471,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974360663301,
        "synchronous_read_wait_us": 61143,
        "system_time_us": 15464,
        "user_time_us": 815564
      },
      {
        "disk_read_elapsed_us": 197382,
        "elapsed_seconds": 0.036,
        "file_descriptor_read_bytes": 92071213,
        "finished_at_unix_us": 1785974369374621,
        "gating": true,
        "os_cpu_virtual_time_us": 116514,
        "os_cpu_wait_time_us": 11393,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 92055121,
        "page_cache_miss_elapsed_us": 196764,
        "peak_memory_bytes": 813528,
        "query_class": "one_hop",
        "query_id": "b730b9c4-9614-57b4-b429-efae8d8cca95",
        "query_name": "q05",
        "read_bytes": 122329664,
        "read_rows": 15291208,
        "real_time_us": 1033793,
        "result_rows": 0,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974369338002,
        "synchronous_read_wait_us": 412175,
        "system_time_us": 46397,
        "user_time_us": 70740
      },
      {
        "disk_read_elapsed_us": 209974,
        "elapsed_seconds": 0.04,
        "file_descriptor_read_bytes": 92389605,
        "finished_at_unix_us": 1785974369777201,
        "gating": true,
        "os_cpu_virtual_time_us": 116110,
        "os_cpu_wait_time_us": 15307,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 92389605,
        "page_cache_miss_elapsed_us": 209663,
        "peak_memory_bytes": 1034563,
        "query_class": "one_hop",
        "query_id": "4c447197-0298-5dcc-863c-bb68268e94b7",
        "query_name": "q05",
        "read_bytes": 122605728,
        "read_rows": 15323976,
        "real_time_us": 979261,
        "result_rows": 46,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974369736968,
        "synchronous_read_wait_us": 275796,
        "system_time_us": 52031,
        "user_time_us": 64614
      },
      {
        "disk_read_elapsed_us": 187221,
        "elapsed_seconds": 0.022,
        "file_descriptor_read_bytes": 92485922,
        "finished_at_unix_us": 1785974370148276,
        "gating": true,
        "os_cpu_virtual_time_us": 110941,
        "os_cpu_wait_time_us": 10068,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 92485922,
        "page_cache_miss_elapsed_us": 186961,
        "peak_memory_bytes": 982147,
        "query_class": "one_hop",
        "query_id": "cecc163f-7a64-5b1a-8a6b-67432d383cf3",
        "query_name": "q05",
        "read_bytes": 122935920,
        "read_rows": 15332168,
        "real_time_us": 595670,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974370126032,
        "synchronous_read_wait_us": 256356,
        "system_time_us": 39798,
        "user_time_us": 71424
      },
      {
        "disk_read_elapsed_us": 0,
        "elapsed_seconds": 0.001,
        "file_descriptor_read_bytes": 0,
        "finished_at_unix_us": 1785974370507307,
        "gating": true,
        "os_cpu_virtual_time_us": 1044,
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
        "real_time_us": 1309,
        "result_rows": 0,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974370506204,
        "synchronous_read_wait_us": 0,
        "system_time_us": 30,
        "user_time_us": 1017
      },
      {
        "disk_read_elapsed_us": 598,
        "elapsed_seconds": 0.003,
        "file_descriptor_read_bytes": 242515,
        "finished_at_unix_us": 1785974370850473,
        "gating": true,
        "os_cpu_virtual_time_us": 5158,
        "os_cpu_wait_time_us": 26,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 242515,
        "page_cache_miss_elapsed_us": 593,
        "peak_memory_bytes": 391348,
        "query_class": "one_hop",
        "query_id": "05433fc9-a0fd-5105-a0bf-222b56ccdaee",
        "query_name": "q05",
        "read_bytes": 276064,
        "read_rows": 32768,
        "real_time_us": 15527,
        "result_rows": 46,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974370847173,
        "synchronous_read_wait_us": 1098,
        "system_time_us": 3446,
        "user_time_us": 1722
      },
      {
        "disk_read_elapsed_us": 782,
        "elapsed_seconds": 0.002,
        "file_descriptor_read_bytes": 444826,
        "finished_at_unix_us": 1785974371177371,
        "gating": true,
        "os_cpu_virtual_time_us": 3478,
        "os_cpu_wait_time_us": 104,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 444826,
        "page_cache_miss_elapsed_us": 777,
        "peak_memory_bytes": 760647,
        "query_class": "one_hop",
        "query_id": "4d1ec754-13eb-50d6-a22c-98ed007e69a9",
        "query_name": "q05",
        "read_bytes": 671792,
        "read_rows": 49152,
        "real_time_us": 11798,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974371174819,
        "synchronous_read_wait_us": 1535,
        "system_time_us": 770,
        "user_time_us": 2717
      },
      {
        "disk_read_elapsed_us": 621,
        "elapsed_seconds": 0.005,
        "file_descriptor_read_bytes": 23951,
        "finished_at_unix_us": 1785974381511847,
        "gating": false,
        "os_cpu_virtual_time_us": 6050,
        "os_cpu_wait_time_us": 419,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 7859,
        "page_cache_miss_elapsed_us": 88,
        "peak_memory_bytes": 512928,
        "query_class": "two_hop",
        "query_id": "e3fe4ac0-fa86-5a02-8efd-25c540966369",
        "query_name": "q06",
        "read_bytes": 65536,
        "read_rows": 8192,
        "real_time_us": 31844,
        "result_rows": 1,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974381506957,
        "synchronous_read_wait_us": 257,
        "system_time_us": 3626,
        "user_time_us": 2441
      },
      {
        "disk_read_elapsed_us": 201291,
        "elapsed_seconds": 0.049,
        "file_descriptor_read_bytes": 110352673,
        "finished_at_unix_us": 1785974381914226,
        "gating": false,
        "os_cpu_virtual_time_us": 168677,
        "os_cpu_wait_time_us": 28532,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 110352673,
        "page_cache_miss_elapsed_us": 200875,
        "peak_memory_bytes": 6273124,
        "query_class": "two_hop",
        "query_id": "9d2e2953-22dd-5b31-b4e5-9cf8066454f2",
        "query_name": "q06",
        "read_bytes": 244869856,
        "read_rows": 15323976,
        "real_time_us": 1229523,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974381865126,
        "synchronous_read_wait_us": 366943,
        "system_time_us": 55949,
        "user_time_us": 113259
      },
      {
        "disk_read_elapsed_us": 206031,
        "elapsed_seconds": 0.03,
        "file_descriptor_read_bytes": 110446614,
        "finished_at_unix_us": 1785974382279227,
        "gating": false,
        "os_cpu_virtual_time_us": 172620,
        "os_cpu_wait_time_us": 28467,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 110446614,
        "page_cache_miss_elapsed_us": 205628,
        "peak_memory_bytes": 10207692,
        "query_class": "two_hop",
        "query_id": "31906d93-f6aa-506e-9e0d-98386489f28e",
        "query_name": "q06",
        "read_bytes": 245200048,
        "read_rows": 15332168,
        "real_time_us": 775991,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974382248949,
        "synchronous_read_wait_us": 288523,
        "system_time_us": 51899,
        "user_time_us": 121177
      },
      {
        "disk_read_elapsed_us": 47,
        "elapsed_seconds": 0.002,
        "file_descriptor_read_bytes": 6052,
        "finished_at_unix_us": 1785974382600708,
        "gating": false,
        "os_cpu_virtual_time_us": 2990,
        "os_cpu_wait_time_us": 19,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 6052,
        "page_cache_miss_elapsed_us": 46,
        "peak_memory_bytes": 498984,
        "query_class": "two_hop",
        "query_id": "8be06a02-9757-5ba0-b974-acaa423bac3f",
        "query_name": "q06",
        "read_bytes": 65536,
        "read_rows": 8192,
        "real_time_us": 19246,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974382598108,
        "synchronous_read_wait_us": 102,
        "system_time_us": 978,
        "user_time_us": 2025
      },
      {
        "disk_read_elapsed_us": 180550,
        "elapsed_seconds": 0.029,
        "file_descriptor_read_bytes": 110608408,
        "finished_at_unix_us": 1785974382976673,
        "gating": false,
        "os_cpu_virtual_time_us": 165533,
        "os_cpu_wait_time_us": 20731,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 110608408,
        "page_cache_miss_elapsed_us": 180219,
        "peak_memory_bytes": 5359812,
        "query_class": "two_hop",
        "query_id": "ca252312-d31a-51f9-97b5-8e8957b9d0f9",
        "query_name": "q06",
        "read_bytes": 244869856,
        "read_rows": 15323976,
        "real_time_us": 729045,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974382947546,
        "synchronous_read_wait_us": 259006,
        "system_time_us": 48992,
        "user_time_us": 116963
      },
      {
        "disk_read_elapsed_us": 173997,
        "elapsed_seconds": 0.028,
        "file_descriptor_read_bytes": 110393926,
        "finished_at_unix_us": 1785974383363786,
        "gating": false,
        "os_cpu_virtual_time_us": 171037,
        "os_cpu_wait_time_us": 23552,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 110393926,
        "page_cache_miss_elapsed_us": 173523,
        "peak_memory_bytes": 10131780,
        "query_class": "two_hop",
        "query_id": "06e16dca-0cb0-5a21-a590-9ab54e9aecf3",
        "query_name": "q06",
        "read_bytes": 245200048,
        "read_rows": 15332168,
        "real_time_us": 698010,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974383335296,
        "synchronous_read_wait_us": 251356,
        "system_time_us": 36854,
        "user_time_us": 134543
      },
      {
        "disk_read_elapsed_us": 76427,
        "elapsed_seconds": 0.173,
        "file_descriptor_read_bytes": 99811611,
        "finished_at_unix_us": 1785974392879294,
        "gating": true,
        "os_cpu_virtual_time_us": 2178012,
        "os_cpu_wait_time_us": 114407,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 99811611,
        "page_cache_miss_elapsed_us": 75701,
        "peak_memory_bytes": 1813299623,
        "query_class": "routine",
        "query_id": "98beb1b8-f4dc-5c3f-8698-b25017f646c8",
        "query_name": "q07",
        "read_bytes": 168113176,
        "read_rows": 15283016,
        "real_time_us": 3789059,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974392706190,
        "synchronous_read_wait_us": 494756,
        "system_time_us": 74239,
        "user_time_us": 2104563
      },
      {
        "disk_read_elapsed_us": 81563,
        "elapsed_seconds": 0.131,
        "file_descriptor_read_bytes": 99761323,
        "finished_at_unix_us": 1785974393365447,
        "gating": true,
        "os_cpu_virtual_time_us": 1820619,
        "os_cpu_wait_time_us": 135163,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 99761323,
        "page_cache_miss_elapsed_us": 80991,
        "peak_memory_bytes": 928596072,
        "query_class": "routine",
        "query_id": "8f02c1e1-b7c5-5c70-90de-d5aac44f331b",
        "query_name": "q07",
        "read_bytes": 168113176,
        "read_rows": 15283016,
        "real_time_us": 2646870,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974393234167,
        "synchronous_read_wait_us": 283057,
        "system_time_us": 41649,
        "user_time_us": 1779507
      },
      {
        "disk_read_elapsed_us": 90360,
        "elapsed_seconds": 0.134,
        "file_descriptor_read_bytes": 99847069,
        "finished_at_unix_us": 1785974393846500,
        "gating": true,
        "os_cpu_virtual_time_us": 1858140,
        "os_cpu_wait_time_us": 144280,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 99847069,
        "page_cache_miss_elapsed_us": 89673,
        "peak_memory_bytes": 928347570,
        "query_class": "routine",
        "query_id": "58755398-ae4b-5258-8d79-71348767369e",
        "query_name": "q07",
        "read_bytes": 168113176,
        "read_rows": 15283016,
        "real_time_us": 2741516,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974393712396,
        "synchronous_read_wait_us": 274434,
        "system_time_us": 35059,
        "user_time_us": 1823626
      },
      {
        "disk_read_elapsed_us": 92530,
        "elapsed_seconds": 0.125,
        "file_descriptor_read_bytes": 99713845,
        "finished_at_unix_us": 1785974394312417,
        "gating": true,
        "os_cpu_virtual_time_us": 1833665,
        "os_cpu_wait_time_us": 63074,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 99713845,
        "page_cache_miss_elapsed_us": 91974,
        "peak_memory_bytes": 932920397,
        "query_class": "routine",
        "query_id": "ca0b271f-58da-5e7a-ae72-b5fb29797641",
        "query_name": "q07",
        "read_bytes": 168113176,
        "read_rows": 15283016,
        "real_time_us": 2580844,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974394186806,
        "synchronous_read_wait_us": 266170,
        "system_time_us": 34122,
        "user_time_us": 1800017
      },
      {
        "disk_read_elapsed_us": 105206,
        "elapsed_seconds": 0.133,
        "file_descriptor_read_bytes": 99761323,
        "finished_at_unix_us": 1785974394808347,
        "gating": true,
        "os_cpu_virtual_time_us": 1840173,
        "os_cpu_wait_time_us": 170118,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 99761323,
        "page_cache_miss_elapsed_us": 104424,
        "peak_memory_bytes": 928630465,
        "query_class": "routine",
        "query_id": "590f6f1c-a94f-543d-9cc9-292c8eca5018",
        "query_name": "q07",
        "read_bytes": 168113176,
        "read_rows": 15283016,
        "real_time_us": 2750715,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974394675030,
        "synchronous_read_wait_us": 310219,
        "system_time_us": 41944,
        "user_time_us": 1798788
      },
      {
        "disk_read_elapsed_us": 92873,
        "elapsed_seconds": 0.128,
        "file_descriptor_read_bytes": 99761323,
        "finished_at_unix_us": 1785974395268341,
        "gating": true,
        "os_cpu_virtual_time_us": 1854864,
        "os_cpu_wait_time_us": 74604,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 99761323,
        "page_cache_miss_elapsed_us": 92113,
        "peak_memory_bytes": 934915765,
        "query_class": "routine",
        "query_id": "37eecc92-ac52-54ae-8794-7f5398c6662d",
        "query_name": "q07",
        "read_bytes": 168113176,
        "read_rows": 15283016,
        "real_time_us": 2631897,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785974395140159,
        "synchronous_read_wait_us": 287524,
        "system_time_us": 37334,
        "user_time_us": 1818183
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
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 30563145
      },
      "timestamp": 1785974270.060747
    },
    {
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 289442729
      },
      "timestamp": 1785974271.290061
    },
    {
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 509119634
      },
      "timestamp": 1785974272.522697
    },
    {
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 721497520
      },
      "timestamp": 1785974273.739831
    },
    {
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 966828240
      },
      "timestamp": 1785974274.948684
    },
    {
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1212214315
      },
      "timestamp": 1785974276.1578062
    },
    {
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1467878419
      },
      "timestamp": 1785974277.375083
    },
    {
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1717698114
      },
      "timestamp": 1785974278.592797
    },
    {
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1960756060
      },
      "timestamp": 1785974279.820838
    },
    {
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2199503771
      },
      "timestamp": 1785974281.059604
    },
    {
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2447034351
      },
      "timestamp": 1785974282.287779
    },
    {
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2664579000
      },
      "timestamp": 1785974283.5230029
    },
    {
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2880037396
      },
      "timestamp": 1785974284.744999
    },
    {
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3104199409
      },
      "timestamp": 1785974285.956612
    },
    {
      "filesystem_bytes": 34212360192,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3406049506
      },
      "timestamp": 1785974287.1459148
    },
    {
      "filesystem_bytes": 43252871168,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3400678783,
        "institutions": 4357308,
        "sources": 10677280,
        "topics": 150309
      },
      "timestamp": 1785974288.346731
    }
  ],
  "tiers": {
    "stage2_large": [
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 45187725
        },
        "timestamp": 1785975806.309257
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 222083671
        },
        "timestamp": 1785975807.5533361
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 354342438
        },
        "timestamp": 1785975808.780343
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 504108365
        },
        "timestamp": 1785975809.993906
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 658197757
        },
        "timestamp": 1785975811.403923
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 658197757
        },
        "timestamp": 1785975812.786747
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 651755336
        },
        "timestamp": 1785975814.157484
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975815.703074
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975817.053617
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975818.345682
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975819.578717
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975820.797607
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975822.1128461
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 173635707,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975823.336021
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 330653224,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975824.580524
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 471054636,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975825.849558
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 611518082,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975827.111479
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 768631521,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975828.3663511
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 909086096,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975829.613423
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1049509539,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975830.86984
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1189127524,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975832.1373801
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1212820781,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975833.398602
      },
      {
        "filesystem_bytes": 37227352064,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1335861623,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975834.653167
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1598651108,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975836.621165
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1673782944,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645140872
        },
        "timestamp": 1785975837.912086
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1657182869,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 65006611,
          "works": 645140872
        },
        "timestamp": 1785975839.251765
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1640600552,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 140188154,
          "works": 645140872
        },
        "timestamp": 1785975840.581385
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1640600552,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 218282932,
          "works": 645140872
        },
        "timestamp": 1785975841.9115279
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1640600552,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 289821457,
          "works": 645140872
        },
        "timestamp": 1785975843.2496388
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1640600552,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 366923417,
          "works": 645140872
        },
        "timestamp": 1785975844.55229
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 447209129,
          "works": 645140872
        },
        "timestamp": 1785975845.855375
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 496274569,
          "works": 645140872
        },
        "timestamp": 1785975847.112133
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 491095851,
          "work_institution": 26782303,
          "works": 645140872
        },
        "timestamp": 1785975848.3629298
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 491095851,
          "work_institution": 53549948,
          "works": 645140872
        },
        "timestamp": 1785975849.597762
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453913990,
          "work_institution": 76924843,
          "works": 645140872
        },
        "timestamp": 1785975850.8365319
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453913990,
          "work_institution": 112552963,
          "works": 645140872
        },
        "timestamp": 1785975852.083512
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453913990,
          "work_institution": 136071289,
          "works": 645140872
        },
        "timestamp": 1785975853.3327942
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453913990,
          "work_institution": 168977785,
          "works": 645140872
        },
        "timestamp": 1785975854.590303
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453913990,
          "work_institution": 204036508,
          "works": 645140872
        },
        "timestamp": 1785975855.8632672
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453913990,
          "work_institution": 236245437,
          "works": 645140872
        },
        "timestamp": 1785975857.118029
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453913990,
          "work_institution": 254104029,
          "works": 645140872
        },
        "timestamp": 1785975858.3522828
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453913990,
          "work_institution": 281488428,
          "works": 645140872
        },
        "timestamp": 1785975859.592248
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453913990,
          "work_institution": 299574797,
          "works": 645140872
        },
        "timestamp": 1785975860.850455
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453913990,
          "work_institution": 299574797,
          "work_topic": 119960275,
          "works": 645140872
        },
        "timestamp": 1785975862.091329
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453913990,
          "work_institution": 299574797,
          "work_topic": 252118515,
          "works": 645140872
        },
        "timestamp": 1785975863.356093
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453913990,
          "work_institution": 299574797,
          "work_topic": 382645571,
          "works": 645140872
        },
        "timestamp": 1785975864.596971
      },
      {
        "filesystem_bytes": 45813547008,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453913990,
          "work_institution": 299574797,
          "work_topic": 501988632,
          "works": 645140872
        },
        "timestamp": 1785975865.871021
      },
      {
        "filesystem_bytes": 47539232768,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453913990,
          "work_institution": 299574797,
          "work_topic": 602626047,
          "works": 645140872
        },
        "timestamp": 1785975867.52321
      }
    ],
    "stage2_medium": [
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 90886177
        },
        "timestamp": 1785974595.9716852
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 220199515
        },
        "timestamp": 1785974597.338086
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 220199515
        },
        "timestamp": 1785974598.6301
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213457735
        },
        "timestamp": 1785974599.8459258
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 89159715,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213457735
        },
        "timestamp": 1785974601.165163
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 207560543,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213457735
        },
        "timestamp": 1785974602.36478
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 348256571,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213457735
        },
        "timestamp": 1785974603.5710158
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 486764979,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213457735
        },
        "timestamp": 1785974604.801344
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 594082577,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213457735
        },
        "timestamp": 1785974606.133538
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 580795609,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 77535623,
          "works": 213457735
        },
        "timestamp": 1785974607.5856519
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 516259860,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 145802689,
          "works": 213457735
        },
        "timestamp": 1785974608.908965
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 516259860,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159086889,
          "works": 213457735
        },
        "timestamp": 1785974610.366079
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 516259860,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159086889,
          "work_institution": 27171114,
          "works": 213457735
        },
        "timestamp": 1785974611.7524748
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 461582913,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159086889,
          "work_institution": 54482931,
          "works": 213457735
        },
        "timestamp": 1785974613.064342
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 461582913,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159086889,
          "work_institution": 78420635,
          "works": 213457735
        },
        "timestamp": 1785974614.351101
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 461582913,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159086889,
          "work_institution": 104064247,
          "work_topic": 30498920,
          "works": 213457735
        },
        "timestamp": 1785974615.610398
      },
      {
        "filesystem_bytes": 44419743744,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 461582913,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159086889,
          "work_institution": 100927174,
          "work_topic": 151766606,
          "works": 213457735
        },
        "timestamp": 1785974616.867027
      },
      {
        "filesystem_bytes": 47383863296,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348758271,
          "citation_edge": 461582913,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159086889,
          "work_institution": 100927174,
          "work_topic": 202442261,
          "works": 213457735
        },
        "timestamp": 1785974618.223371
      }
    ],
    "stage2_small": [
      {
        "filesystem_bytes": 43920265216,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3371627220,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 43851570
        },
        "timestamp": 1785974291.4254951
      },
      {
        "filesystem_bytes": 43920265216,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3371627220,
          "citation_edge": 119673473,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 43851570
        },
        "timestamp": 1785974292.693738
      },
      {
        "filesystem_bytes": 43920265216,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3371627220,
          "citation_edge": 107586178,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 40617754,
          "work_institution": 23570968,
          "works": 43851570
        },
        "timestamp": 1785974293.9271328
      },
      {
        "filesystem_bytes": 44878639104,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3371627220,
          "citation_edge": 107586178,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 40617754,
          "work_institution": 23570968,
          "work_topic": 38954929,
          "works": 43851570
        },
        "timestamp": 1785974294.9159849
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
- stage2_small: the canonical Authors snapshot leaves 8133 of 3852081 Work-author bridge rows unresolved, including 8118 documented NULL-author rows and 0 documented deleted-author rows. The ordinary unresolved count is 15 of 3843963 (coverage 0.9999960978; blocking floor 0.999000). Raw links are preserved; use LEFT JOIN when unmatched authorships matter.
- stage2_medium: the canonical Authors snapshot leaves 33354 of 16075482 Work-author bridge rows unresolved, including 33089 documented NULL-author rows and 0 documented deleted-author rows. The ordinary unresolved count is 265 of 16042393 (coverage 0.9999834813; blocking floor 0.999000). Raw links are preserved; use LEFT JOIN when unmatched authorships matter.
- stage2_large: the canonical Authors snapshot leaves 98331 of 51816498 Work-author bridge rows unresolved, including 93593 documented NULL-author rows and 0 documented deleted-author rows. The ordinary unresolved count is 4738 of 51722905 (coverage 0.9999083965; blocking floor 0.999000). Raw links are preserved; use LEFT JOIN when unmatched authorships matter.
