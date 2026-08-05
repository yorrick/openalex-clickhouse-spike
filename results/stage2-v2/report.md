# OpenAlex ClickHouse validation — stage2-v2

Local engine verdict: fail

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
      "docker_memory_bytes": 50427109376,
      "memory_bytes": 34359738368,
      "nano_cpus": 16000000000
    }
  },
  "inputs": {
    "complete_authors_bytes": 52769910496,
    "maximum_raw_input_bytes": 98301763421,
    "run_identity": {
      "config_sha256": "f30f5dc8ff0d754e60a9bddb803e8d91d249e262ce077766939744e13853e818",
      "download_state_sha256": "c01aa4ecf6f9b005eb14120b6de797a3e70a2c727a5e15254b6f6a8ef11a939e",
      "memory_gib": 32,
      "rendered_sql_sha256": {
        "00_schema.sql": "4ae827e545557298bd567861365b110789a6d97eca99b10850d42471e659537f",
        "11_load_complete_authors.sql": "2c6af303c4ce11947291b4c60d2dcfc4208ec36cb0076427221a0b4a4dabacd8",
        "12_load_small_dimensions.sql": "f5bc794b3d20b4bdbdb515ac18b3fc967283d16f278e2569f9f9b007d6530976",
        "30_reverse_projection.sql": "13310a4c542ed9f37bd4a52ef448db44c9c4537964a4a0dfd99da246f08b8296",
        "stage2_large/05_raw_evidence.sql": "093f45e5f4da6e10fdc41cd301d1c2822866d11da167f74d1c753c8e1e84bbf5",
        "stage2_large/20_load_works.sql": "c220f71ec0057821ec40b6c142df86e42431a8e7815eae08f5cb3c4720948069",
        "stage2_medium/05_raw_evidence.sql": "486472a3a3a3ec5a2b11d965c4933a6bce4c1bd35dbdb31fe2d694f1c8d40e5a",
        "stage2_medium/20_load_works.sql": "892bb666e6e0f5aa16e9d526120997c7e3665c2b9c393fe450a790890e7e7fc4",
        "stage2_small/05_raw_evidence.sql": "797a7ccfaecba47b213e1664e925a39e284aeed47a89b71106934db9f0950681",
        "stage2_small/20_load_works.sql": "e985ab0d1a17fab23ffd6bcd939b44b760d0e86a96527bf0a4ad13d93ccd851b"
      },
      "run_id": "stage2-v2",
      "selection_sha256": "ccc7b5c51f04bd5972e6fb513f15157c13a79300be5fc5c36696aebbf56026b1",
      "sha256": "0d826a565d3cbd4809485871099846d7a1a1c79c4693ceed9e2ea2141e19131d",
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
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.works) AS works, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author) AS authors, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_institution) AS institutions, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_topic) AS topics, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.citation_edge) AS citations",
        "sql_sha256": "d0839ae8ba340e187b9184b8a8d7b27f76c0e0afe7fff4b64f3bc730ee44a4cf"
      },
      {
        "name": "referential_coverage",
        "result_row_count": 1,
        "result_sha256": "97a87bcbd1e7199e574988b6c7ebc35e1cb86ab5bc2e171e387b43c4013534fe",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.works w ON wa.work_id=w.work_id) AS missing_works_for_authors, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author) AS author_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id) AS missing_authors, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id) AS distinct_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id) AS works_with_missing_authors, if(author_bridge_rows = 0, 1., 1 - missing_authors / author_bridge_rows) AS author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author WHERE author_id=9999999999) AS null_author_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author WHERE author_id=5317838346) AS deleted_author_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author WHERE author_id NOT IN (9999999999,5317838346)) AS ordinary_authorship_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS ordinary_missing_author_rows, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS distinct_ordinary_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS works_with_ordinary_missing_authors, if(ordinary_authorship_rows = 0, 1., 1 - ordinary_missing_author_rows / ordinary_authorship_rows) AS ordinary_author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_institution) AS institution_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) AS missing_institutions, (SELECT uniqExact(wi.institution_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) AS distinct_missing_institution_ids, (SELECT uniqExact(wi.work_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) AS works_with_missing_institutions, (SELECT uniqExact(wi.author_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) AS authors_with_missing_institutions, if(institution_bridge_rows = 0, 1., (institution_bridge_rows - missing_institutions) / institution_bridge_rows) AS institution_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_topic) AS topic_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.topics t ON wt.topic_id=t.topic_id) AS missing_topics, (SELECT uniqExact(wt.topic_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.topics t ON wt.topic_id=t.topic_id) AS distinct_missing_topic_ids, if(topic_bridge_rows = 0, 1., (topic_bridge_rows - missing_topics) / topic_bridge_rows) AS topic_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.citation_edge) AS citation_edges, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.citation_edge ce INNER JOIN openalex_stage2_stage2_v2_ae9ae799.works w ON ce.cited_work_id=w.work_id) AS retained_cited_edges, if(citation_edges = 0, 1., retained_cited_edges / citation_edges) AS citation_retention_ratio",
        "sql_sha256": "99cdd2116fe44017c8d3ff28f72d18b2ef81e9d574ebe2cda6abf186f8556e78"
      },
      {
        "name": "missing_author_sample",
        "result_row_count": 25,
        "result_sha256": "44359b4810798de7ec48cf6afb714bab06c06352e3a0b1b9d5ddd4284d670dbe",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wa.author_id FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id) SELECT openalex_numeric_id(authorship.author.id) AS author_id, multiIf(author_id=9999999999, 'null_author', author_id=5317838346, 'deleted_author', 'ordinary') AS classification, arraySlice(arraySort(groupUniqArray(ifNull(authorship.author.display_name, ''))), 1, 5) AS display_names, count() AS raw_bridge_rows FROM file('tiers/stage2_large/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship WHERE openalex_numeric_id(authorship.author.id) IN missing_ids GROUP BY author_id ORDER BY raw_bridge_rows DESC, author_id LIMIT 25",
        "sql_sha256": "2493916861d19ef781ada3e04c73fc65a1c6b1ee3626c188c36388efa32e85f2"
      },
      {
        "name": "missing_institution_sample",
        "result_row_count": 25,
        "result_sha256": "0a5d7a24775cc990e0818eb12f1d49eedfbd8ffa2d44d159193ecceb3427c05a",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wi.institution_id FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) SELECT openalex_numeric_id(raw_institution.id) AS institution_id, any(raw_institution.display_name) AS display_name, count() AS raw_bridge_rows FROM file('tiers/stage2_large/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship ARRAY JOIN authorship.institutions AS raw_institution WHERE openalex_numeric_id(raw_institution.id) IN missing_ids GROUP BY institution_id ORDER BY raw_bridge_rows DESC, institution_id LIMIT 25",
        "sql_sha256": "89acf1d3ccf533df3e5f9cec8b1640bf989645486a7045b66292bfafddc8101a"
      },
      {
        "name": "works_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "eec0816fb4eaeb19b8e4f555e3bcc79a63a63336b547593e4c25222d510d205e",
        "sql": "SELECT count() AS rows, uniqExact(work_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.works",
        "sql_sha256": "7d902cedda9ad8f4782c4128bc77b8052c88f9ec2c2a22c5a62e957f001f8f9d"
      },
      {
        "name": "authors_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "ad147b0c2afdbf81139c75c21696b85568b9bd6db2c30818e5fe0d962e8a0170",
        "sql": "SELECT count() AS rows, uniqExact(author_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.authors",
        "sql_sha256": "9b2e7353ca0321ad7b8da264d5889f797dd05254073e22f24bbaca63a607abfa"
      },
      {
        "name": "institutions_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "1d729a2ea001d72722af893931308d2a7ffb55562e2a5a3c33945a1cc15f9c47",
        "sql": "SELECT count() AS rows, uniqExact(institution_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.institutions",
        "sql_sha256": "60b6e6d973c748bb38d2098d0656b8d78e25c1336574a7423b336623b23937cc"
      },
      {
        "name": "sources_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "8515fa4a030ad72ca441f50ae103ac1b7701fb65366d5de9dab09a297ce71e9f",
        "sql": "SELECT count() AS rows, uniqExact(source_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.sources",
        "sql_sha256": "62f1f433576644207158a4bbee61e4ac6f516efb33f2b93af3684823a9c74a82"
      },
      {
        "name": "topics_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "83708a811c93190b16a1b7dbe7033261c7a31e9cc7d70ade69ae253c50e5ac75",
        "sql": "SELECT count() AS rows, uniqExact(topic_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.topics",
        "sql_sha256": "8b71acab34e5bb7fb995110e6d3c512195b63c0c912cc15693f5f65a6b854482"
      },
      {
        "name": "year_type_topic_xpac_distribution",
        "result_row_count": 2201659,
        "result_sha256": "687cd62516f49aa16089bac525ce076838eeb289cadba49f0bf4c99b9192028f",
        "sql": "SELECT publication_year, work_type, primary_topic_id, is_xpac, count() AS works FROM openalex_stage2_stage2_v2_ae9ae799.works GROUP BY ALL ORDER BY ALL",
        "sql_sha256": "4962eaae56e9319deb1bb8371ea8a5371af6e4d9d18435c4c3ccae779d6265f7"
      },
      {
        "name": "authorships_per_work",
        "result_row_count": 843,
        "result_sha256": "6265ea4756058c8ed86bfe5c3b998dec58901617cbb497a620400b6f1d78d37a",
        "sql": "SELECT authorships, count() AS works FROM (SELECT work_id, count() AS authorships FROM openalex_stage2_stage2_v2_ae9ae799.work_author GROUP BY work_id) GROUP BY authorships ORDER BY authorships",
        "sql_sha256": "05494bfc88dcb0c1dc776d2b641f606fb49ce52588f58f1d7c28d817532608ac"
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
      "20_load_works.sql": "c220f71ec0057821ec40b6c142df86e42431a8e7815eae08f5cb3c4720948069"
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
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.works) AS works, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author) AS authors, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_institution) AS institutions, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_topic) AS topics, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.citation_edge) AS citations",
        "sql_sha256": "d0839ae8ba340e187b9184b8a8d7b27f76c0e0afe7fff4b64f3bc730ee44a4cf"
      },
      {
        "name": "referential_coverage",
        "result_row_count": 1,
        "result_sha256": "9bfc14c04fcf4b2beb8ad257b9bc2d24f9e5b9f486bac539bfa8a33728e53a50",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.works w ON wa.work_id=w.work_id) AS missing_works_for_authors, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author) AS author_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id) AS missing_authors, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id) AS distinct_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id) AS works_with_missing_authors, if(author_bridge_rows = 0, 1., 1 - missing_authors / author_bridge_rows) AS author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author WHERE author_id=9999999999) AS null_author_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author WHERE author_id=5317838346) AS deleted_author_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author WHERE author_id NOT IN (9999999999,5317838346)) AS ordinary_authorship_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS ordinary_missing_author_rows, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS distinct_ordinary_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS works_with_ordinary_missing_authors, if(ordinary_authorship_rows = 0, 1., 1 - ordinary_missing_author_rows / ordinary_authorship_rows) AS ordinary_author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_institution) AS institution_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) AS missing_institutions, (SELECT uniqExact(wi.institution_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) AS distinct_missing_institution_ids, (SELECT uniqExact(wi.work_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) AS works_with_missing_institutions, (SELECT uniqExact(wi.author_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) AS authors_with_missing_institutions, if(institution_bridge_rows = 0, 1., (institution_bridge_rows - missing_institutions) / institution_bridge_rows) AS institution_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_topic) AS topic_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.topics t ON wt.topic_id=t.topic_id) AS missing_topics, (SELECT uniqExact(wt.topic_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.topics t ON wt.topic_id=t.topic_id) AS distinct_missing_topic_ids, if(topic_bridge_rows = 0, 1., (topic_bridge_rows - missing_topics) / topic_bridge_rows) AS topic_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.citation_edge) AS citation_edges, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.citation_edge ce INNER JOIN openalex_stage2_stage2_v2_ae9ae799.works w ON ce.cited_work_id=w.work_id) AS retained_cited_edges, if(citation_edges = 0, 1., retained_cited_edges / citation_edges) AS citation_retention_ratio",
        "sql_sha256": "99cdd2116fe44017c8d3ff28f72d18b2ef81e9d574ebe2cda6abf186f8556e78"
      },
      {
        "name": "missing_author_sample",
        "result_row_count": 25,
        "result_sha256": "2029b08cef3cc2b317e2e92a98c1c91cfbed1f75ef27fafca4b6a895f7c9fc95",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wa.author_id FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id) SELECT openalex_numeric_id(authorship.author.id) AS author_id, multiIf(author_id=9999999999, 'null_author', author_id=5317838346, 'deleted_author', 'ordinary') AS classification, arraySlice(arraySort(groupUniqArray(ifNull(authorship.author.display_name, ''))), 1, 5) AS display_names, count() AS raw_bridge_rows FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship WHERE openalex_numeric_id(authorship.author.id) IN missing_ids GROUP BY author_id ORDER BY raw_bridge_rows DESC, author_id LIMIT 25",
        "sql_sha256": "259b4684dd1d3c78e2f34ee2381166fd68393dbba859eda198a5eec9dc149af7"
      },
      {
        "name": "missing_institution_sample",
        "result_row_count": 25,
        "result_sha256": "041d556c79b9cc31f860bd11a2eb21e1f96d47e8e9ce9c80b50b2f84fd9f03c5",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wi.institution_id FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) SELECT openalex_numeric_id(raw_institution.id) AS institution_id, any(raw_institution.display_name) AS display_name, count() AS raw_bridge_rows FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship ARRAY JOIN authorship.institutions AS raw_institution WHERE openalex_numeric_id(raw_institution.id) IN missing_ids GROUP BY institution_id ORDER BY raw_bridge_rows DESC, institution_id LIMIT 25",
        "sql_sha256": "8194db984a9e779ccdb5f397128d67816c799a86843d95e7293e64fc43b125a5"
      },
      {
        "name": "works_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "56aabad587204e1a393c30baf149217c0ee158c3b8434f32e4eba7ae0aae34cf",
        "sql": "SELECT count() AS rows, uniqExact(work_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.works",
        "sql_sha256": "7d902cedda9ad8f4782c4128bc77b8052c88f9ec2c2a22c5a62e957f001f8f9d"
      },
      {
        "name": "authors_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "ad147b0c2afdbf81139c75c21696b85568b9bd6db2c30818e5fe0d962e8a0170",
        "sql": "SELECT count() AS rows, uniqExact(author_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.authors",
        "sql_sha256": "9b2e7353ca0321ad7b8da264d5889f797dd05254073e22f24bbaca63a607abfa"
      },
      {
        "name": "institutions_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "1d729a2ea001d72722af893931308d2a7ffb55562e2a5a3c33945a1cc15f9c47",
        "sql": "SELECT count() AS rows, uniqExact(institution_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.institutions",
        "sql_sha256": "60b6e6d973c748bb38d2098d0656b8d78e25c1336574a7423b336623b23937cc"
      },
      {
        "name": "sources_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "8515fa4a030ad72ca441f50ae103ac1b7701fb65366d5de9dab09a297ce71e9f",
        "sql": "SELECT count() AS rows, uniqExact(source_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.sources",
        "sql_sha256": "62f1f433576644207158a4bbee61e4ac6f516efb33f2b93af3684823a9c74a82"
      },
      {
        "name": "topics_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "83708a811c93190b16a1b7dbe7033261c7a31e9cc7d70ade69ae253c50e5ac75",
        "sql": "SELECT count() AS rows, uniqExact(topic_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.topics",
        "sql_sha256": "8b71acab34e5bb7fb995110e6d3c512195b63c0c912cc15693f5f65a6b854482"
      },
      {
        "name": "year_type_topic_xpac_distribution",
        "result_row_count": 1307378,
        "result_sha256": "9fd1a41a5f5bc8119582c700239d950531afec5124792c9998806df498e7da42",
        "sql": "SELECT publication_year, work_type, primary_topic_id, is_xpac, count() AS works FROM openalex_stage2_stage2_v2_ae9ae799.works GROUP BY ALL ORDER BY ALL",
        "sql_sha256": "4962eaae56e9319deb1bb8371ea8a5371af6e4d9d18435c4c3ccae779d6265f7"
      },
      {
        "name": "authorships_per_work",
        "result_row_count": 447,
        "result_sha256": "2bc843d8da3f9998d26c7d558b7c8464e08af5a43f8e0128f60d3aa4c3f77d9e",
        "sql": "SELECT authorships, count() AS works FROM (SELECT work_id, count() AS authorships FROM openalex_stage2_stage2_v2_ae9ae799.work_author GROUP BY work_id) GROUP BY authorships ORDER BY authorships",
        "sql_sha256": "05494bfc88dcb0c1dc776d2b641f606fb49ce52588f58f1d7c28d817532608ac"
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
      "20_load_works.sql": "892bb666e6e0f5aa16e9d526120997c7e3665c2b9c393fe450a790890e7e7fc4"
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
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.works) AS works, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author) AS authors, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_institution) AS institutions, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_topic) AS topics, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.citation_edge) AS citations",
        "sql_sha256": "d0839ae8ba340e187b9184b8a8d7b27f76c0e0afe7fff4b64f3bc730ee44a4cf"
      },
      {
        "name": "referential_coverage",
        "result_row_count": 1,
        "result_sha256": "aaacea8bab04a1689cbd1580515b55fb7b21aa9a3ec549a22df8b6c55a6add54",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.works w ON wa.work_id=w.work_id) AS missing_works_for_authors, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author) AS author_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id) AS missing_authors, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id) AS distinct_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id) AS works_with_missing_authors, if(author_bridge_rows = 0, 1., 1 - missing_authors / author_bridge_rows) AS author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author WHERE author_id=9999999999) AS null_author_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author WHERE author_id=5317838346) AS deleted_author_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author WHERE author_id NOT IN (9999999999,5317838346)) AS ordinary_authorship_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS ordinary_missing_author_rows, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS distinct_ordinary_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS works_with_ordinary_missing_authors, if(ordinary_authorship_rows = 0, 1., 1 - ordinary_missing_author_rows / ordinary_authorship_rows) AS ordinary_author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_institution) AS institution_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) AS missing_institutions, (SELECT uniqExact(wi.institution_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) AS distinct_missing_institution_ids, (SELECT uniqExact(wi.work_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) AS works_with_missing_institutions, (SELECT uniqExact(wi.author_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) AS authors_with_missing_institutions, if(institution_bridge_rows = 0, 1., (institution_bridge_rows - missing_institutions) / institution_bridge_rows) AS institution_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_topic) AS topic_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.topics t ON wt.topic_id=t.topic_id) AS missing_topics, (SELECT uniqExact(wt.topic_id) FROM openalex_stage2_stage2_v2_ae9ae799.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.topics t ON wt.topic_id=t.topic_id) AS distinct_missing_topic_ids, if(topic_bridge_rows = 0, 1., (topic_bridge_rows - missing_topics) / topic_bridge_rows) AS topic_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.citation_edge) AS citation_edges, (SELECT count() FROM openalex_stage2_stage2_v2_ae9ae799.citation_edge ce INNER JOIN openalex_stage2_stage2_v2_ae9ae799.works w ON ce.cited_work_id=w.work_id) AS retained_cited_edges, if(citation_edges = 0, 1., retained_cited_edges / citation_edges) AS citation_retention_ratio",
        "sql_sha256": "99cdd2116fe44017c8d3ff28f72d18b2ef81e9d574ebe2cda6abf186f8556e78"
      },
      {
        "name": "missing_author_sample",
        "result_row_count": 14,
        "result_sha256": "99a76bcebd2eb596aad11499de36d0f0433fdd046319d0bec9237a41f9f28082",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wa.author_id FROM openalex_stage2_stage2_v2_ae9ae799.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.authors a ON wa.author_id=a.author_id) SELECT openalex_numeric_id(authorship.author.id) AS author_id, multiIf(author_id=9999999999, 'null_author', author_id=5317838346, 'deleted_author', 'ordinary') AS classification, arraySlice(arraySort(groupUniqArray(ifNull(authorship.author.display_name, ''))), 1, 5) AS display_names, count() AS raw_bridge_rows FROM file('tiers/stage2_small/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship WHERE openalex_numeric_id(authorship.author.id) IN missing_ids GROUP BY author_id ORDER BY raw_bridge_rows DESC, author_id LIMIT 25",
        "sql_sha256": "8a3040a136f6ca885201658f67a6a27854ebf9a8febdbc2b7affc51cc46fd9fc"
      },
      {
        "name": "missing_institution_sample",
        "result_row_count": 25,
        "result_sha256": "e76891d77558501c47c0f69c20680983202e0d65482fb85bfcbd131b4f66f365",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wi.institution_id FROM openalex_stage2_stage2_v2_ae9ae799.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_v2_ae9ae799.institutions i ON wi.institution_id=i.institution_id) SELECT openalex_numeric_id(raw_institution.id) AS institution_id, any(raw_institution.display_name) AS display_name, count() AS raw_bridge_rows FROM file('tiers/stage2_small/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship ARRAY JOIN authorship.institutions AS raw_institution WHERE openalex_numeric_id(raw_institution.id) IN missing_ids GROUP BY institution_id ORDER BY raw_bridge_rows DESC, institution_id LIMIT 25",
        "sql_sha256": "6b8e2630ac495640693ee65967bd2bc76745d2aadb79aa400cfc588717dc8f53"
      },
      {
        "name": "works_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "74a4b54bd6c6fe3b72ff60e9d31fff2d02e1622bd0a05fa63ef21325131ac1b5",
        "sql": "SELECT count() AS rows, uniqExact(work_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.works",
        "sql_sha256": "7d902cedda9ad8f4782c4128bc77b8052c88f9ec2c2a22c5a62e957f001f8f9d"
      },
      {
        "name": "authors_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "ad147b0c2afdbf81139c75c21696b85568b9bd6db2c30818e5fe0d962e8a0170",
        "sql": "SELECT count() AS rows, uniqExact(author_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.authors",
        "sql_sha256": "9b2e7353ca0321ad7b8da264d5889f797dd05254073e22f24bbaca63a607abfa"
      },
      {
        "name": "institutions_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "1d729a2ea001d72722af893931308d2a7ffb55562e2a5a3c33945a1cc15f9c47",
        "sql": "SELECT count() AS rows, uniqExact(institution_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.institutions",
        "sql_sha256": "60b6e6d973c748bb38d2098d0656b8d78e25c1336574a7423b336623b23937cc"
      },
      {
        "name": "sources_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "8515fa4a030ad72ca441f50ae103ac1b7701fb65366d5de9dab09a297ce71e9f",
        "sql": "SELECT count() AS rows, uniqExact(source_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.sources",
        "sql_sha256": "62f1f433576644207158a4bbee61e4ac6f516efb33f2b93af3684823a9c74a82"
      },
      {
        "name": "topics_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "83708a811c93190b16a1b7dbe7033261c7a31e9cc7d70ade69ae253c50e5ac75",
        "sql": "SELECT count() AS rows, uniqExact(topic_id) AS unique_ids FROM openalex_stage2_stage2_v2_ae9ae799.topics",
        "sql_sha256": "8b71acab34e5bb7fb995110e6d3c512195b63c0c912cc15693f5f65a6b854482"
      },
      {
        "name": "year_type_topic_xpac_distribution",
        "result_row_count": 492399,
        "result_sha256": "89b42e728db3c8983e10ef0e5324c51deb698afea5daa05dcefcf53b0917024e",
        "sql": "SELECT publication_year, work_type, primary_topic_id, is_xpac, count() AS works FROM openalex_stage2_stage2_v2_ae9ae799.works GROUP BY ALL ORDER BY ALL",
        "sql_sha256": "4962eaae56e9319deb1bb8371ea8a5371af6e4d9d18435c4c3ccae779d6265f7"
      },
      {
        "name": "authorships_per_work",
        "result_row_count": 200,
        "result_sha256": "8c704127e6d040ac4779ce338b625f61ecd0f9a7faee500ee1f59850b8dc3b38",
        "sql": "SELECT authorships, count() AS works FROM (SELECT work_id, count() AS authorships FROM openalex_stage2_stage2_v2_ae9ae799.work_author GROUP BY work_id) GROUP BY authorships ORDER BY authorships",
        "sql_sha256": "05494bfc88dcb0c1dc776d2b641f606fb49ce52588f58f1d7c28d817532608ac"
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
      "20_load_works.sql": "e985ab0d1a17fab23ffd6bcd939b44b760d0e86a96527bf0a4ad13d93ccd851b"
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
          "count": 155,
          "insufficient_sample": false,
          "maximum_seconds": 146.503,
          "median_seconds": 19.165,
          "p95_seconds": 140.781
        },
        "one_hop": {
          "count": 50,
          "insufficient_sample": false,
          "maximum_seconds": 0.658,
          "median_seconds": 0.01,
          "p95_seconds": 0.476
        },
        "routine": {
          "count": 99,
          "insufficient_sample": false,
          "maximum_seconds": 18.145,
          "median_seconds": 0.269,
          "p95_seconds": 16.874
        }
      },
      "first_error": null,
      "forced_verdict": null,
      "server_restarted": false,
      "verdict_cap": "pass"
    },
    "stage2_medium": {
      "classes": {
        "join": {
          "count": 155,
          "insufficient_sample": false,
          "maximum_seconds": 20.061,
          "median_seconds": 4.49,
          "p95_seconds": 19.099
        },
        "one_hop": {
          "count": 51,
          "insufficient_sample": false,
          "maximum_seconds": 0.13,
          "median_seconds": 0.004,
          "p95_seconds": 0.106
        },
        "routine": {
          "count": 99,
          "insufficient_sample": false,
          "maximum_seconds": 4.997,
          "median_seconds": 0.101,
          "p95_seconds": 4.802
        }
      },
      "first_error": null,
      "forced_verdict": null,
      "server_restarted": false,
      "verdict_cap": "pass"
    },
    "stage2_small": {
      "classes": {
        "join": {
          "count": 154,
          "insufficient_sample": false,
          "maximum_seconds": 1.863,
          "median_seconds": 0.405,
          "p95_seconds": 1.7
        },
        "one_hop": {
          "count": 51,
          "insufficient_sample": false,
          "maximum_seconds": 0.048,
          "median_seconds": 0.005,
          "p95_seconds": 0.026
        },
        "routine": {
          "count": 99,
          "insufficient_sample": false,
          "maximum_seconds": 0.407,
          "median_seconds": 0.033,
          "p95_seconds": 0.391
        }
      },
      "first_error": null,
      "forced_verdict": null,
      "server_restarted": false,
      "verdict_cap": "pass"
    }
  },
  "sequential": {
    "stage2_large": [
      {
        "elapsed_seconds": 0.13,
        "gating": true,
        "peak_memory_bytes": 108824780,
        "query_class": "routine",
        "query_id": "df512afc-6dbe-5945-a5d1-e55bf577bf44",
        "query_name": "q01",
        "read_bytes": 191311446,
        "read_rows": 31885241,
        "result_rows": 11928,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.104,
        "gating": true,
        "peak_memory_bytes": 108588371,
        "query_class": "routine",
        "query_id": "daf2a53e-c750-5e2f-860b-e1505cfea366",
        "query_name": "q01",
        "read_bytes": 191311446,
        "read_rows": 31885241,
        "result_rows": 11928,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.1,
        "gating": true,
        "peak_memory_bytes": 108652608,
        "query_class": "routine",
        "query_id": "d3bb4593-4c92-5135-a170-ffa8c6570ed0",
        "query_name": "q01",
        "read_bytes": 191311446,
        "read_rows": 31885241,
        "result_rows": 11928,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.094,
        "gating": true,
        "peak_memory_bytes": 108378480,
        "query_class": "routine",
        "query_id": "5a32df48-5741-5587-ac89-9ce3aba1a9ab",
        "query_name": "q01",
        "read_bytes": 191311446,
        "read_rows": 31885241,
        "result_rows": 11928,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.063,
        "gating": true,
        "peak_memory_bytes": 109458582,
        "query_class": "routine",
        "query_id": "e04f25c3-0733-5e23-9720-f93eefba728d",
        "query_name": "q01",
        "read_bytes": 191311446,
        "read_rows": 31885241,
        "result_rows": 11928,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.058,
        "gating": true,
        "peak_memory_bytes": 107463157,
        "query_class": "routine",
        "query_id": "3f5f661e-7b16-5e6b-8061-a243b02826cf",
        "query_name": "q01",
        "read_bytes": 191311446,
        "read_rows": 31885241,
        "result_rows": 11928,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 66.996,
        "gating": true,
        "peak_memory_bytes": 2229770724,
        "query_class": "join",
        "query_id": "13595f55-8ce6-5f96-9afd-a4a8889d126a",
        "query_name": "q02",
        "read_bytes": 1511924436,
        "read_rows": 96479335,
        "result_rows": 838464,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 66.012,
        "gating": true,
        "peak_memory_bytes": 2216882353,
        "query_class": "join",
        "query_id": "a2848046-3ec2-5022-963e-ecd8f76e25e6",
        "query_name": "q02",
        "read_bytes": 1511924436,
        "read_rows": 96479335,
        "result_rows": 838464,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 68.061,
        "gating": true,
        "peak_memory_bytes": 2212498863,
        "query_class": "join",
        "query_id": "5504b261-1dca-5b3c-a586-47a9e9403c20",
        "query_name": "q02",
        "read_bytes": 1511924436,
        "read_rows": 96479335,
        "result_rows": 838464,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 66.445,
        "gating": true,
        "peak_memory_bytes": 2206597013,
        "query_class": "join",
        "query_id": "edd03e6a-5f6b-5a3c-9c5b-bc50f3eddaad",
        "query_name": "q02",
        "read_bytes": 1511924436,
        "read_rows": 96479335,
        "result_rows": 838464,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 66.641,
        "gating": true,
        "peak_memory_bytes": 2225453148,
        "query_class": "join",
        "query_id": "bfad4687-cb42-5ffe-bbec-e399dc66ffac",
        "query_name": "q02",
        "read_bytes": 1511924436,
        "read_rows": 96479335,
        "result_rows": 838464,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 65.981,
        "gating": true,
        "peak_memory_bytes": 2224277778,
        "query_class": "join",
        "query_id": "c63b7a6c-1bb7-5a2d-8f4b-edc4eb13fe71",
        "query_name": "q02",
        "read_bytes": 1511924436,
        "read_rows": 96479335,
        "result_rows": 838464,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 9.709,
        "gating": true,
        "peak_memory_bytes": 3484974199,
        "query_class": "join",
        "query_id": "55a2bf14-7bc6-50bb-b8f8-e7afc7b5a6d8",
        "query_name": "q03",
        "read_bytes": 4369474957,
        "read_rows": 202831399,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 9.908,
        "gating": true,
        "peak_memory_bytes": 3677085612,
        "query_class": "join",
        "query_id": "68b45e30-86bb-5487-9691-09331c63a648",
        "query_name": "q03",
        "read_bytes": 4369474957,
        "read_rows": 202831399,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 10.184,
        "gating": true,
        "peak_memory_bytes": 3486836547,
        "query_class": "join",
        "query_id": "c3ea97aa-7c10-5851-805d-648e39c76f4d",
        "query_name": "q03",
        "read_bytes": 4369474957,
        "read_rows": 202831399,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 10.264,
        "gating": true,
        "peak_memory_bytes": 3492366099,
        "query_class": "join",
        "query_id": "02ca305d-ad37-5cb1-a79a-a037ed6dc1df",
        "query_name": "q03",
        "read_bytes": 4369474957,
        "read_rows": 202831399,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 9.972,
        "gating": true,
        "peak_memory_bytes": 3499555394,
        "query_class": "join",
        "query_id": "5e44ed1a-1a6c-53c4-963f-15b1773e443c",
        "query_name": "q03",
        "read_bytes": 4369474957,
        "read_rows": 202831399,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 9.998,
        "gating": true,
        "peak_memory_bytes": 3447503845,
        "query_class": "join",
        "query_id": "940ad897-60ba-5c49-9760-e4c1df1d7253",
        "query_name": "q03",
        "read_bytes": 4369474957,
        "read_rows": 202831399,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 11.863,
        "gating": true,
        "peak_memory_bytes": 4647071086,
        "query_class": "join",
        "query_id": "7ba2143e-1129-5b61-aa62-5815d203c396",
        "query_name": "q04",
        "read_bytes": 1619556399,
        "read_rows": 111140203,
        "result_rows": 173617,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 12.033,
        "gating": true,
        "peak_memory_bytes": 4658497550,
        "query_class": "join",
        "query_id": "cedb075c-63d5-5b0e-95b3-395ba6ca4d9a",
        "query_name": "q04",
        "read_bytes": 1619556399,
        "read_rows": 111140203,
        "result_rows": 173617,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 12.231,
        "gating": true,
        "peak_memory_bytes": 4636427484,
        "query_class": "join",
        "query_id": "9801aa14-b9e6-5fd2-b51f-036a8ddf9c9a",
        "query_name": "q04",
        "read_bytes": 1619556399,
        "read_rows": 111140203,
        "result_rows": 173617,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 12.202,
        "gating": true,
        "peak_memory_bytes": 4643453605,
        "query_class": "join",
        "query_id": "cac9576c-5bbd-5797-b028-2d781cf4f7c1",
        "query_name": "q04",
        "read_bytes": 1619556399,
        "read_rows": 111140203,
        "result_rows": 173617,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 12.039,
        "gating": true,
        "peak_memory_bytes": 4644128477,
        "query_class": "join",
        "query_id": "0810c65e-2c98-5cd1-b43c-bfb4c95a789a",
        "query_name": "q04",
        "read_bytes": 1619556399,
        "read_rows": 111140203,
        "result_rows": 173617,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 12.168,
        "gating": true,
        "peak_memory_bytes": 4640539799,
        "query_class": "join",
        "query_id": "3b30e5aa-2e1a-5868-8c48-f7db737325cd",
        "query_name": "q04",
        "read_bytes": 1619556399,
        "read_rows": 111140203,
        "result_rows": 173617,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.257,
        "gating": true,
        "peak_memory_bytes": 5787240,
        "query_class": "one_hop",
        "query_id": "b730b9c4-9614-57b4-b429-efae8d8cca95",
        "query_name": "q05",
        "read_bytes": 1670821784,
        "read_rows": 208852723,
        "result_rows": 0,
        "run_kind": "post_restart_run",
        "seed_work_id": 25441,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.25,
        "gating": true,
        "peak_memory_bytes": 5776227,
        "query_class": "one_hop",
        "query_id": "4c447197-0298-5dcc-863c-bb68268e94b7",
        "query_name": "q05",
        "read_bytes": 1671096368,
        "read_rows": 208852723,
        "result_rows": 48,
        "run_kind": "warm_run",
        "seed_work_id": 1491165,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.242,
        "gating": true,
        "peak_memory_bytes": 5853888,
        "query_class": "one_hop",
        "query_id": "cecc163f-7a64-5b1a-8a6b-67432d383cf3",
        "query_name": "q05",
        "read_bytes": 1671218272,
        "read_rows": 208852723,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "seed_work_id": 4388957908,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.001,
        "gating": true,
        "peak_memory_bytes": 317072,
        "query_class": "one_hop",
        "query_id": "56847c14-8888-5648-b76e-e6bcc1efb0fe",
        "query_name": "q05",
        "read_bytes": 0,
        "read_rows": 0,
        "result_rows": 0,
        "run_kind": "warm_run",
        "seed_work_id": 25441,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.01,
        "gating": true,
        "peak_memory_bytes": 448683,
        "query_class": "one_hop",
        "query_id": "05433fc9-a0fd-5105-a0bf-222b56ccdaee",
        "query_name": "q05",
        "read_bytes": 1585304,
        "read_rows": 163840,
        "result_rows": 48,
        "run_kind": "warm_run",
        "seed_work_id": 1491165,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.003,
        "gating": true,
        "peak_memory_bytes": 781657,
        "query_class": "one_hop",
        "query_id": "4d1ec754-13eb-50d6-a22c-98ed007e69a9",
        "query_name": "q05",
        "read_bytes": 920776,
        "read_rows": 65536,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "seed_work_id": 4388957908,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.036,
        "gating": false,
        "peak_memory_bytes": 548592,
        "query_class": "two_hop",
        "query_id": "e3fe4ac0-fa86-5a02-8efd-25c540966369",
        "query_name": "q06",
        "read_bytes": 524288,
        "read_rows": 65536,
        "result_rows": 1,
        "run_kind": "post_restart_run",
        "seed_work_id": 25441,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.423,
        "gating": false,
        "peak_memory_bytes": 9717036,
        "query_class": "two_hop",
        "query_id": "9d2e2953-22dd-5b31-b4e5-9cf8066454f2",
        "query_name": "q06",
        "read_bytes": 3341347016,
        "read_rows": 208852723,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 1491165,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.305,
        "gating": false,
        "peak_memory_bytes": 17381210,
        "query_class": "two_hop",
        "query_id": "31906d93-f6aa-506e-9e0d-98386489f28e",
        "query_name": "q06",
        "read_bytes": 3341515768,
        "read_rows": 208852723,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 4388957908,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.004,
        "gating": false,
        "peak_memory_bytes": 511536,
        "query_class": "two_hop",
        "query_id": "8be06a02-9757-5ba0-b974-acaa423bac3f",
        "query_name": "q06",
        "read_bytes": 524288,
        "read_rows": 65536,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 25441,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.302,
        "gating": false,
        "peak_memory_bytes": 12196248,
        "query_class": "two_hop",
        "query_id": "ca252312-d31a-51f9-97b5-8e8957b9d0f9",
        "query_name": "q06",
        "read_bytes": 3341347016,
        "read_rows": 208852723,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 1491165,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.311,
        "gating": false,
        "peak_memory_bytes": 18456174,
        "query_class": "two_hop",
        "query_id": "06e16dca-0cb0-5a21-a590-9ab54e9aecf3",
        "query_name": "q06",
        "read_bytes": 3341515768,
        "read_rows": 208852723,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 4388957908,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 4.002,
        "gating": true,
        "peak_memory_bytes": 4186650179,
        "query_class": "routine",
        "query_id": "98beb1b8-f4dc-5c3f-8698-b25017f646c8",
        "query_name": "q07",
        "read_bytes": 2296659057,
        "read_rows": 208787187,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 4.089,
        "gating": true,
        "peak_memory_bytes": 3925743755,
        "query_class": "routine",
        "query_id": "8f02c1e1-b7c5-5c70-90de-d5aac44f331b",
        "query_name": "q07",
        "read_bytes": 2296659057,
        "read_rows": 208787187,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 4.121,
        "gating": true,
        "peak_memory_bytes": 3517896307,
        "query_class": "routine",
        "query_id": "58755398-ae4b-5258-8d79-71348767369e",
        "query_name": "q07",
        "read_bytes": 2296659057,
        "read_rows": 208787187,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 4.128,
        "gating": true,
        "peak_memory_bytes": 3449988410,
        "query_class": "routine",
        "query_id": "ca0b271f-58da-5e7a-ae72-b5fb29797641",
        "query_name": "q07",
        "read_bytes": 2296659057,
        "read_rows": 208787187,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 4.155,
        "gating": true,
        "peak_memory_bytes": 3812865699,
        "query_class": "routine",
        "query_id": "590f6f1c-a94f-543d-9cc9-292c8eca5018",
        "query_name": "q07",
        "read_bytes": 2296659057,
        "read_rows": 208787187,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 4.247,
        "gating": true,
        "peak_memory_bytes": 3541751583,
        "query_class": "routine",
        "query_id": "37eecc92-ac52-54ae-8794-7f5398c6662d",
        "query_name": "q07",
        "read_bytes": 2296659057,
        "read_rows": 208787187,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      }
    ],
    "stage2_medium": [
      {
        "elapsed_seconds": 0.058,
        "gating": true,
        "peak_memory_bytes": 106980668,
        "query_class": "routine",
        "query_id": "df512afc-6dbe-5945-a5d1-e55bf577bf44",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "result_rows": 9810,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.045,
        "gating": true,
        "peak_memory_bytes": 108236126,
        "query_class": "routine",
        "query_id": "daf2a53e-c750-5e2f-860b-e1505cfea366",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.025,
        "gating": true,
        "peak_memory_bytes": 108043948,
        "query_class": "routine",
        "query_id": "d3bb4593-4c92-5135-a170-ffa8c6570ed0",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.024,
        "gating": true,
        "peak_memory_bytes": 108258051,
        "query_class": "routine",
        "query_id": "5a32df48-5741-5587-ac89-9ce3aba1a9ab",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.025,
        "gating": true,
        "peak_memory_bytes": 108125123,
        "query_class": "routine",
        "query_id": "e04f25c3-0733-5e23-9720-f93eefba728d",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.026,
        "gating": true,
        "peak_memory_bytes": 109118555,
        "query_class": "routine",
        "query_id": "3f5f661e-7b16-5e6b-8061-a243b02826cf",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 10.062,
        "gating": true,
        "peak_memory_bytes": 2220160579,
        "query_class": "join",
        "query_id": "13595f55-8ce6-5f96-9afd-a4a8889d126a",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "result_rows": 579800,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 10.019,
        "gating": true,
        "peak_memory_bytes": 2288420724,
        "query_class": "join",
        "query_id": "a2848046-3ec2-5022-963e-ecd8f76e25e6",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 10.457,
        "gating": true,
        "peak_memory_bytes": 2309797565,
        "query_class": "join",
        "query_id": "5504b261-1dca-5b3c-a586-47a9e9403c20",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 10.357,
        "gating": true,
        "peak_memory_bytes": 2247293320,
        "query_class": "join",
        "query_id": "edd03e6a-5f6b-5a3c-9c5b-bc50f3eddaad",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 10.225,
        "gating": true,
        "peak_memory_bytes": 2263457803,
        "query_class": "join",
        "query_id": "bfad4687-cb42-5ffe-bbec-e399dc66ffac",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 10.551,
        "gating": true,
        "peak_memory_bytes": 2234899672,
        "query_class": "join",
        "query_id": "c63b7a6c-1bb7-5a2d-8f4b-edc4eb13fe71",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 2.67,
        "gating": true,
        "peak_memory_bytes": 2192286422,
        "query_class": "join",
        "query_id": "55a2bf14-7bc6-50bb-b8f8-e7afc7b5a6d8",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 2.671,
        "gating": true,
        "peak_memory_bytes": 2253411024,
        "query_class": "join",
        "query_id": "68b45e30-86bb-5487-9691-09331c63a648",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 2.711,
        "gating": true,
        "peak_memory_bytes": 2263493246,
        "query_class": "join",
        "query_id": "c3ea97aa-7c10-5851-805d-648e39c76f4d",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 2.801,
        "gating": true,
        "peak_memory_bytes": 2191699257,
        "query_class": "join",
        "query_id": "02ca305d-ad37-5cb1-a79a-a037ed6dc1df",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 2.721,
        "gating": true,
        "peak_memory_bytes": 2231387246,
        "query_class": "join",
        "query_id": "5e44ed1a-1a6c-53c4-963f-15b1773e443c",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 2.768,
        "gating": true,
        "peak_memory_bytes": 2249223724,
        "query_class": "join",
        "query_id": "940ad897-60ba-5c49-9760-e4c1df1d7253",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 2.427,
        "gating": true,
        "peak_memory_bytes": 2203776039,
        "query_class": "join",
        "query_id": "7ba2143e-1129-5b61-aa62-5815d203c396",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "result_rows": 110456,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 2.353,
        "gating": true,
        "peak_memory_bytes": 2206313258,
        "query_class": "join",
        "query_id": "cedb075c-63d5-5b0e-95b3-395ba6ca4d9a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 2.417,
        "gating": true,
        "peak_memory_bytes": 2204080859,
        "query_class": "join",
        "query_id": "9801aa14-b9e6-5fd2-b51f-036a8ddf9c9a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 2.458,
        "gating": true,
        "peak_memory_bytes": 2211075971,
        "query_class": "join",
        "query_id": "cac9576c-5bbd-5797-b028-2d781cf4f7c1",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 2.446,
        "gating": true,
        "peak_memory_bytes": 2200857841,
        "query_class": "join",
        "query_id": "0810c65e-2c98-5cd1-b43c-bfb4c95a789a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 2.454,
        "gating": true,
        "peak_memory_bytes": 2192008329,
        "query_class": "join",
        "query_id": "3b30e5aa-2e1a-5868-8c48-f7db737325cd",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.104,
        "gating": true,
        "peak_memory_bytes": 2171664,
        "query_class": "one_hop",
        "query_id": "b730b9c4-9614-57b4-b429-efae8d8cca95",
        "query_name": "q05",
        "read_bytes": 563458944,
        "read_rows": 70432368,
        "result_rows": 0,
        "run_kind": "post_restart_run",
        "seed_work_id": 25441,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.085,
        "gating": true,
        "peak_memory_bytes": 2162742,
        "query_class": "one_hop",
        "query_id": "4c447197-0298-5dcc-863c-bb68268e94b7",
        "query_name": "q05",
        "read_bytes": 563555736,
        "read_rows": 70432368,
        "result_rows": 46,
        "run_kind": "warm_run",
        "seed_work_id": 1491165,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.086,
        "gating": true,
        "peak_memory_bytes": 2243494,
        "query_class": "one_hop",
        "query_id": "cecc163f-7a64-5b1a-8a6b-67432d383cf3",
        "query_name": "q05",
        "read_bytes": 563590016,
        "read_rows": 70432368,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "seed_work_id": 4388957908,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.001,
        "gating": true,
        "peak_memory_bytes": 317072,
        "query_class": "one_hop",
        "query_id": "56847c14-8888-5648-b76e-e6bcc1efb0fe",
        "query_name": "q05",
        "read_bytes": 0,
        "read_rows": 0,
        "result_rows": 0,
        "run_kind": "warm_run",
        "seed_work_id": 25441,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.006,
        "gating": true,
        "peak_memory_bytes": 355078,
        "query_class": "one_hop",
        "query_id": "05433fc9-a0fd-5105-a0bf-222b56ccdaee",
        "query_name": "q05",
        "read_bytes": 227864,
        "read_rows": 16384,
        "result_rows": 46,
        "run_kind": "warm_run",
        "seed_work_id": 1491165,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.002,
        "gating": true,
        "peak_memory_bytes": 435366,
        "query_class": "one_hop",
        "query_id": "4d1ec754-13eb-50d6-a22c-98ed007e69a9",
        "query_name": "q05",
        "read_bytes": 262144,
        "read_rows": 16384,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "seed_work_id": 4388957908,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.004,
        "gating": false,
        "peak_memory_bytes": 493936,
        "query_class": "two_hop",
        "query_id": "e3fe4ac0-fa86-5a02-8efd-25c540966369",
        "query_name": "q06",
        "read_bytes": 131072,
        "read_rows": 16384,
        "result_rows": 1,
        "run_kind": "post_restart_run",
        "seed_work_id": 25441,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.092,
        "gating": false,
        "peak_memory_bytes": 7404689,
        "query_class": "two_hop",
        "query_id": "9d2e2953-22dd-5b31-b4e5-9cf8066454f2",
        "query_name": "q06",
        "read_bytes": 1126883608,
        "read_rows": 70432368,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 1491165,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.099,
        "gating": false,
        "peak_memory_bytes": 12231302,
        "query_class": "two_hop",
        "query_id": "31906d93-f6aa-506e-9e0d-98386489f28e",
        "query_name": "q06",
        "read_bytes": 1126917888,
        "read_rows": 70432368,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 4388957908,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.003,
        "gating": false,
        "peak_memory_bytes": 467368,
        "query_class": "two_hop",
        "query_id": "8be06a02-9757-5ba0-b974-acaa423bac3f",
        "query_name": "q06",
        "read_bytes": 131072,
        "read_rows": 16384,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 25441,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.1,
        "gating": false,
        "peak_memory_bytes": 3836077,
        "query_class": "two_hop",
        "query_id": "ca252312-d31a-51f9-97b5-8e8957b9d0f9",
        "query_name": "q06",
        "read_bytes": 1126883608,
        "read_rows": 70432368,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 1491165,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.1,
        "gating": false,
        "peak_memory_bytes": 11039000,
        "query_class": "two_hop",
        "query_id": "06e16dca-0cb0-5a21-a590-9ab54e9aecf3",
        "query_name": "q06",
        "read_bytes": 1126917888,
        "read_rows": 70432368,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 4388957908,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 1.256,
        "gating": true,
        "peak_memory_bytes": 4236537597,
        "query_class": "routine",
        "query_id": "98beb1b8-f4dc-5c3f-8698-b25017f646c8",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 1.227,
        "gating": true,
        "peak_memory_bytes": 3966184573,
        "query_class": "routine",
        "query_id": "8f02c1e1-b7c5-5c70-90de-d5aac44f331b",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 1.216,
        "gating": true,
        "peak_memory_bytes": 3363937925,
        "query_class": "routine",
        "query_id": "58755398-ae4b-5258-8d79-71348767369e",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 1.214,
        "gating": true,
        "peak_memory_bytes": 3763702013,
        "query_class": "routine",
        "query_id": "ca0b271f-58da-5e7a-ae72-b5fb29797641",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 1.231,
        "gating": true,
        "peak_memory_bytes": 3141246389,
        "query_class": "routine",
        "query_id": "590f6f1c-a94f-543d-9cc9-292c8eca5018",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 1.246,
        "gating": true,
        "peak_memory_bytes": 3464486101,
        "query_class": "routine",
        "query_id": "37eecc92-ac52-54ae-8794-7f5398c6662d",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      }
    ],
    "stage2_small": [
      {
        "elapsed_seconds": 0.033,
        "gating": true,
        "peak_memory_bytes": 61809417,
        "query_class": "routine",
        "query_id": "df512afc-6dbe-5945-a5d1-e55bf577bf44",
        "query_name": "q01",
        "read_bytes": 12017892,
        "read_rows": 2002982,
        "result_rows": 6174,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.013,
        "gating": true,
        "peak_memory_bytes": 63003135,
        "query_class": "routine",
        "query_id": "daf2a53e-c750-5e2f-860b-e1505cfea366",
        "query_name": "q01",
        "read_bytes": 12017892,
        "read_rows": 2002982,
        "result_rows": 6174,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.012,
        "gating": true,
        "peak_memory_bytes": 63596199,
        "query_class": "routine",
        "query_id": "d3bb4593-4c92-5135-a170-ffa8c6570ed0",
        "query_name": "q01",
        "read_bytes": 12017892,
        "read_rows": 2002982,
        "result_rows": 6174,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.013,
        "gating": true,
        "peak_memory_bytes": 61183728,
        "query_class": "routine",
        "query_id": "5a32df48-5741-5587-ac89-9ce3aba1a9ab",
        "query_name": "q01",
        "read_bytes": 12017892,
        "read_rows": 2002982,
        "result_rows": 6174,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.014,
        "gating": true,
        "peak_memory_bytes": 64086423,
        "query_class": "routine",
        "query_id": "e04f25c3-0733-5e23-9720-f93eefba728d",
        "query_name": "q01",
        "read_bytes": 12017892,
        "read_rows": 2002982,
        "result_rows": 6174,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.012,
        "gating": true,
        "peak_memory_bytes": 63619479,
        "query_class": "routine",
        "query_id": "3f5f661e-7b16-5e6b-8061-a243b02826cf",
        "query_name": "q01",
        "read_bytes": 12017892,
        "read_rows": 2002982,
        "result_rows": 6174,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.256,
        "gating": true,
        "peak_memory_bytes": 1162641599,
        "query_class": "join",
        "query_id": "13595f55-8ce6-5f96-9afd-a4a8889d126a",
        "query_name": "q02",
        "read_bytes": 96483111,
        "read_rows": 6146611,
        "result_rows": 346801,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.232,
        "gating": true,
        "peak_memory_bytes": 1130883448,
        "query_class": "join",
        "query_id": "a2848046-3ec2-5022-963e-ecd8f76e25e6",
        "query_name": "q02",
        "read_bytes": 96483111,
        "read_rows": 6146611,
        "result_rows": 346801,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.234,
        "gating": true,
        "peak_memory_bytes": 1134619554,
        "query_class": "join",
        "query_id": "5504b261-1dca-5b3c-a586-47a9e9403c20",
        "query_name": "q02",
        "read_bytes": 96483111,
        "read_rows": 6146611,
        "result_rows": 346801,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.235,
        "gating": true,
        "peak_memory_bytes": 1131430363,
        "query_class": "join",
        "query_id": "edd03e6a-5f6b-5a3c-9c5b-bc50f3eddaad",
        "query_name": "q02",
        "read_bytes": 96483111,
        "read_rows": 6146611,
        "result_rows": 346801,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.228,
        "gating": true,
        "peak_memory_bytes": 1124670700,
        "query_class": "join",
        "query_id": "bfad4687-cb42-5ffe-bbec-e399dc66ffac",
        "query_name": "q02",
        "read_bytes": 96483111,
        "read_rows": 6146611,
        "result_rows": 346801,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.238,
        "gating": true,
        "peak_memory_bytes": 1118524800,
        "query_class": "join",
        "query_id": "c63b7a6c-1bb7-5a2d-8f4b-edc4eb13fe71",
        "query_name": "q02",
        "read_bytes": 96483111,
        "read_rows": 6146611,
        "result_rows": 346801,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.966,
        "gating": true,
        "peak_memory_bytes": 2197689544,
        "query_class": "join",
        "query_id": "55a2bf14-7bc6-50bb-b8f8-e7afc7b5a6d8",
        "query_name": "q03",
        "read_bytes": 3243457177,
        "read_rows": 124984723,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.962,
        "gating": true,
        "peak_memory_bytes": 2186477087,
        "query_class": "join",
        "query_id": "68b45e30-86bb-5487-9691-09331c63a648",
        "query_name": "q03",
        "read_bytes": 3243457177,
        "read_rows": 124984723,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.977,
        "gating": true,
        "peak_memory_bytes": 2176241707,
        "query_class": "join",
        "query_id": "c3ea97aa-7c10-5851-805d-648e39c76f4d",
        "query_name": "q03",
        "read_bytes": 3243457177,
        "read_rows": 124984723,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.978,
        "gating": true,
        "peak_memory_bytes": 2209528476,
        "query_class": "join",
        "query_id": "02ca305d-ad37-5cb1-a79a-a037ed6dc1df",
        "query_name": "q03",
        "read_bytes": 3243457177,
        "read_rows": 124984723,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.988,
        "gating": true,
        "peak_memory_bytes": 2195976099,
        "query_class": "join",
        "query_id": "5e44ed1a-1a6c-53c4-963f-15b1773e443c",
        "query_name": "q03",
        "read_bytes": 3243457177,
        "read_rows": 124984723,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.999,
        "gating": true,
        "peak_memory_bytes": 2176038876,
        "query_class": "join",
        "query_id": "940ad897-60ba-5c49-9760-e4c1df1d7253",
        "query_name": "q03",
        "read_bytes": 3243457177,
        "read_rows": 124984723,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.352,
        "gating": true,
        "peak_memory_bytes": 668060570,
        "query_class": "join",
        "query_id": "7ba2143e-1129-5b61-aa62-5815d203c396",
        "query_name": "q04",
        "read_bytes": 111540414,
        "read_rows": 7550998,
        "result_rows": 54471,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.307,
        "gating": true,
        "peak_memory_bytes": 676805547,
        "query_class": "join",
        "query_id": "cedb075c-63d5-5b0e-95b3-395ba6ca4d9a",
        "query_name": "q04",
        "read_bytes": 111540414,
        "read_rows": 7550998,
        "result_rows": 54471,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.309,
        "gating": true,
        "peak_memory_bytes": 685046674,
        "query_class": "join",
        "query_id": "9801aa14-b9e6-5fd2-b51f-036a8ddf9c9a",
        "query_name": "q04",
        "read_bytes": 111540414,
        "read_rows": 7550998,
        "result_rows": 54471,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.312,
        "gating": true,
        "peak_memory_bytes": 666524743,
        "query_class": "join",
        "query_id": "cac9576c-5bbd-5797-b028-2d781cf4f7c1",
        "query_name": "q04",
        "read_bytes": 111540414,
        "read_rows": 7550998,
        "result_rows": 54471,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.307,
        "gating": true,
        "peak_memory_bytes": 679050027,
        "query_class": "join",
        "query_id": "0810c65e-2c98-5cd1-b43c-bfb4c95a789a",
        "query_name": "q04",
        "read_bytes": 111540414,
        "read_rows": 7550998,
        "result_rows": 54471,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.31,
        "gating": true,
        "peak_memory_bytes": 679303096,
        "query_class": "join",
        "query_id": "3b30e5aa-2e1a-5868-8c48-f7db737325cd",
        "query_name": "q04",
        "read_bytes": 111540414,
        "read_rows": 7550998,
        "result_rows": 54471,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.043,
        "gating": true,
        "peak_memory_bytes": 802200,
        "query_class": "one_hop",
        "query_id": "b730b9c4-9614-57b4-b429-efae8d8cca95",
        "query_name": "q05",
        "read_bytes": 122329664,
        "read_rows": 15291208,
        "result_rows": 0,
        "run_kind": "post_restart_run",
        "seed_work_id": 25441,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.022,
        "gating": true,
        "peak_memory_bytes": 851164,
        "query_class": "one_hop",
        "query_id": "4c447197-0298-5dcc-863c-bb68268e94b7",
        "query_name": "q05",
        "read_bytes": 122605728,
        "read_rows": 15323976,
        "result_rows": 46,
        "run_kind": "warm_run",
        "seed_work_id": 1491165,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.022,
        "gating": true,
        "peak_memory_bytes": 976792,
        "query_class": "one_hop",
        "query_id": "cecc163f-7a64-5b1a-8a6b-67432d383cf3",
        "query_name": "q05",
        "read_bytes": 122935920,
        "read_rows": 15332168,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "seed_work_id": 4388957908,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.001,
        "gating": true,
        "peak_memory_bytes": 317072,
        "query_class": "one_hop",
        "query_id": "56847c14-8888-5648-b76e-e6bcc1efb0fe",
        "query_name": "q05",
        "read_bytes": 0,
        "read_rows": 0,
        "result_rows": 0,
        "run_kind": "warm_run",
        "seed_work_id": 25441,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.003,
        "gating": true,
        "peak_memory_bytes": 386748,
        "query_class": "one_hop",
        "query_id": "05433fc9-a0fd-5105-a0bf-222b56ccdaee",
        "query_name": "q05",
        "read_bytes": 276064,
        "read_rows": 32768,
        "result_rows": 46,
        "run_kind": "warm_run",
        "seed_work_id": 1491165,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.002,
        "gating": true,
        "peak_memory_bytes": 760086,
        "query_class": "one_hop",
        "query_id": "4d1ec754-13eb-50d6-a22c-98ed007e69a9",
        "query_name": "q05",
        "read_bytes": 671792,
        "read_rows": 49152,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "seed_work_id": 4388957908,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.004,
        "gating": false,
        "peak_memory_bytes": 489424,
        "query_class": "two_hop",
        "query_id": "e3fe4ac0-fa86-5a02-8efd-25c540966369",
        "query_name": "q06",
        "read_bytes": 65536,
        "read_rows": 8192,
        "result_rows": 1,
        "run_kind": "post_restart_run",
        "seed_work_id": 25441,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.053,
        "gating": false,
        "peak_memory_bytes": 6046094,
        "query_class": "two_hop",
        "query_id": "9d2e2953-22dd-5b31-b4e5-9cf8066454f2",
        "query_name": "q06",
        "read_bytes": 244869856,
        "read_rows": 15323976,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 1491165,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.029,
        "gating": false,
        "peak_memory_bytes": 9729510,
        "query_class": "two_hop",
        "query_id": "31906d93-f6aa-506e-9e0d-98386489f28e",
        "query_name": "q06",
        "read_bytes": 245200048,
        "read_rows": 15332168,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 4388957908,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.002,
        "gating": false,
        "peak_memory_bytes": 468656,
        "query_class": "two_hop",
        "query_id": "8be06a02-9757-5ba0-b974-acaa423bac3f",
        "query_name": "q06",
        "read_bytes": 65536,
        "read_rows": 8192,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 25441,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.03,
        "gating": false,
        "peak_memory_bytes": 5327042,
        "query_class": "two_hop",
        "query_id": "ca252312-d31a-51f9-97b5-8e8957b9d0f9",
        "query_name": "q06",
        "read_bytes": 244869856,
        "read_rows": 15323976,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 1491165,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.03,
        "gating": false,
        "peak_memory_bytes": 8651399,
        "query_class": "two_hop",
        "query_id": "06e16dca-0cb0-5a21-a590-9ab54e9aecf3",
        "query_name": "q06",
        "read_bytes": 245200048,
        "read_rows": 15332168,
        "result_rows": 1,
        "run_kind": "warm_run",
        "seed_work_id": 4388957908,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.18,
        "gating": true,
        "peak_memory_bytes": 1611852823,
        "query_class": "routine",
        "query_id": "98beb1b8-f4dc-5c3f-8698-b25017f646c8",
        "query_name": "q07",
        "read_bytes": 168113176,
        "read_rows": 15283016,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.143,
        "gating": true,
        "peak_memory_bytes": 858144005,
        "query_class": "routine",
        "query_id": "8f02c1e1-b7c5-5c70-90de-d5aac44f331b",
        "query_name": "q07",
        "read_bytes": 168113176,
        "read_rows": 15283016,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.142,
        "gating": true,
        "peak_memory_bytes": 856168526,
        "query_class": "routine",
        "query_id": "58755398-ae4b-5258-8d79-71348767369e",
        "query_name": "q07",
        "read_bytes": 168113176,
        "read_rows": 15283016,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.151,
        "gating": true,
        "peak_memory_bytes": 943299103,
        "query_class": "routine",
        "query_id": "ca0b271f-58da-5e7a-ae72-b5fb29797641",
        "query_name": "q07",
        "read_bytes": 168113176,
        "read_rows": 15283016,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.148,
        "gating": true,
        "peak_memory_bytes": 858912757,
        "query_class": "routine",
        "query_id": "590f6f1c-a94f-543d-9cc9-292c8eca5018",
        "query_name": "q07",
        "read_bytes": 168113176,
        "read_rows": 15283016,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 0.139,
        "gating": true,
        "peak_memory_bytes": 852110963,
        "query_class": "routine",
        "query_id": "37eecc92-ac52-54ae-8794-7f5398c6662d",
        "query_name": "q07",
        "read_bytes": 168113176,
        "read_rows": 15283016,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
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
      "filesystem_bytes": 4880502784,
      "projection_bytes": {},
      "table_bytes": {},
      "timestamp": 1785899903.990342
    },
    {
      "filesystem_bytes": 4880502784,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 288824495
      },
      "timestamp": 1785899905.201231
    },
    {
      "filesystem_bytes": 4880502784,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 540159124
      },
      "timestamp": 1785899906.412123
    },
    {
      "filesystem_bytes": 4880502784,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 809468159
      },
      "timestamp": 1785899907.619893
    },
    {
      "filesystem_bytes": 4880502784,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1090176525
      },
      "timestamp": 1785899908.822328
    },
    {
      "filesystem_bytes": 4880502784,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1340831062
      },
      "timestamp": 1785899910.026846
    },
    {
      "filesystem_bytes": 4880502784,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1622335662
      },
      "timestamp": 1785899911.241597
    },
    {
      "filesystem_bytes": 4880502784,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1898614701
      },
      "timestamp": 1785899912.463697
    },
    {
      "filesystem_bytes": 4880502784,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2173676045
      },
      "timestamp": 1785899913.69887
    },
    {
      "filesystem_bytes": 4880502784,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2419672870
      },
      "timestamp": 1785899914.923947
    },
    {
      "filesystem_bytes": 4880502784,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2692530306
      },
      "timestamp": 1785899916.159415
    },
    {
      "filesystem_bytes": 4880502784,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2946284065
      },
      "timestamp": 1785899917.3731961
    },
    {
      "filesystem_bytes": 4880502784,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3195664210
      },
      "timestamp": 1785899918.592119
    },
    {
      "filesystem_bytes": 13851217920,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3400380453,
        "institutions": 4357308,
        "sources": 10677280,
        "topics": 150309
      },
      "timestamp": 1785899919.708231
    }
  ],
  "tiers": {
    "stage2_large": [
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 134197854
        },
        "timestamp": 1785900930.873185
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 292736393
        },
        "timestamp": 1785900932.123929
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 422203085
        },
        "timestamp": 1785900933.3528981
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 577109495
        },
        "timestamp": 1785900934.581568
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 658101818
        },
        "timestamp": 1785900935.924105
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 651893260
        },
        "timestamp": 1785900937.266748
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900938.553687
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900939.863022
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900941.207256
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900942.48257
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900943.696604
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900944.987822
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 104161393,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900946.212878
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 278542872,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900947.465676
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 418957977,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900948.689652
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 558604453,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900949.933463
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 699138928,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900951.175373
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 839600132,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900952.428937
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1014023981,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900953.6944609
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1154382337,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900954.944156
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1294797246,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900956.20286
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1317701478,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900957.445652
      },
      {
        "filesystem_bytes": 9965948928,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1475555754,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900958.664225
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1657182869,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645310606
        },
        "timestamp": 1785900961.241333
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1640600552,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 86552999,
          "works": 645310606
        },
        "timestamp": 1785900962.543435
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1640600552,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 156265111,
          "works": 645310606
        },
        "timestamp": 1785900963.846488
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1640600552,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 239869284,
          "works": 645310606
        },
        "timestamp": 1785900965.200806
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1640600552,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 319829363,
          "works": 645310606
        },
        "timestamp": 1785900966.5477262
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 393511670,
          "works": 645310606
        },
        "timestamp": 1785900967.882439
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 475157975,
          "works": 645310606
        },
        "timestamp": 1785900969.1331
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 490950619,
          "work_institution": 9437968,
          "works": 645310606
        },
        "timestamp": 1785900970.408247
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 490950619,
          "work_institution": 35953041,
          "works": 645310606
        },
        "timestamp": 1785900971.657102
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 490950619,
          "work_institution": 58781911,
          "works": 645310606
        },
        "timestamp": 1785900972.91585
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 94073346,
          "works": 645310606
        },
        "timestamp": 1785900974.1770399
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 117753673,
          "works": 645310606
        },
        "timestamp": 1785900975.382713
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 144740720,
          "works": 645310606
        },
        "timestamp": 1785900976.6363819
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 177970065,
          "works": 645310606
        },
        "timestamp": 1785900977.890989
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 204371170,
          "works": 645310606
        },
        "timestamp": 1785900979.153131
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 236074770,
          "works": 645310606
        },
        "timestamp": 1785900980.420269
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 253725913,
          "works": 645310606
        },
        "timestamp": 1785900981.675589
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 262665691,
          "works": 645310606
        },
        "timestamp": 1785900982.9317381
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 273297230,
          "works": 645310606
        },
        "timestamp": 1785900984.185815
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 299646471,
          "work_topic": 50025877,
          "works": 645310606
        },
        "timestamp": 1785900985.443962
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 299646471,
          "work_topic": 179441763,
          "works": 645310606
        },
        "timestamp": 1785900986.6890008
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 299646471,
          "work_topic": 301279844,
          "works": 645310606
        },
        "timestamp": 1785900987.94105
      },
      {
        "filesystem_bytes": 18575585280,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 299646471,
          "work_topic": 422662042,
          "works": 645310606
        },
        "timestamp": 1785900989.1818838
      },
      {
        "filesystem_bytes": 19856375808,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 299646471,
          "work_topic": 600914890,
          "works": 645310606
        },
        "timestamp": 1785900991.634513
      },
      {
        "filesystem_bytes": 20211445760,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453989434,
          "work_institution": 299646471,
          "work_topic": 600914890,
          "works": 645310606
        },
        "timestamp": 1785900991.844245
      }
    ],
    "stage2_medium": [
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 44408252
        },
        "timestamp": 1785900129.820711
      },
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 220322533
        },
        "timestamp": 1785900131.098301
      },
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213746575
        },
        "timestamp": 1785900132.342299
      },
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213746575
        },
        "timestamp": 1785900133.617454
      },
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 100326536,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213746575
        },
        "timestamp": 1785900134.885432
      },
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 229861899,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213746575
        },
        "timestamp": 1785900136.079415
      },
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 368395625,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213746575
        },
        "timestamp": 1785900137.2664378
      },
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 520232319,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213746575
        },
        "timestamp": 1785900138.486544
      },
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 580786218,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 32321185,
          "works": 213746575
        },
        "timestamp": 1785900139.793679
      },
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 580786218,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 133562614,
          "works": 213746575
        },
        "timestamp": 1785900141.0337129
      },
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 516250207,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159103960,
          "work_institution": 9268293,
          "works": 213746575
        },
        "timestamp": 1785900142.28422
      },
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159103960,
          "work_institution": 45488540,
          "works": 213746575
        },
        "timestamp": 1785900143.529552
      },
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159103960,
          "work_institution": 78326617,
          "works": 213746575
        },
        "timestamp": 1785900144.760621
      },
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159103960,
          "work_institution": 100958401,
          "work_topic": 40772538,
          "works": 213746575
        },
        "timestamp": 1785900145.983982
      },
      {
        "filesystem_bytes": 15723909120,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159103960,
          "work_institution": 100958401,
          "work_topic": 172032296,
          "works": 213746575
        },
        "timestamp": 1785900147.203472
      },
      {
        "filesystem_bytes": 18647650304,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348574835,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159103960,
          "work_institution": 100958401,
          "work_topic": 202429019,
          "works": 213746575
        },
        "timestamp": 1785900147.496523
      }
    ],
    "stage2_small": [
      {
        "filesystem_bytes": 14470103040,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3371374672,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309
        },
        "timestamp": 1785899922.53851
      },
      {
        "filesystem_bytes": 14470103040,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3371374672,
          "citation_edge": 101557351,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 43832861
        },
        "timestamp": 1785899923.745089
      },
      {
        "filesystem_bytes": 14470103040,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3371374672,
          "citation_edge": 107586178,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 40605412,
          "works": 43832861
        },
        "timestamp": 1785899924.9497888
      },
      {
        "filesystem_bytes": 15428153344,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3371374672,
          "citation_edge": 107586178,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 40605412,
          "work_institution": 23580788,
          "work_topic": 38948393,
          "works": 43832861
        },
        "timestamp": 1785899925.620755
      }
    ]
  }
}
```

Scaling slopes are empirical evidence from sampled tiers; they are not a full-size prediction.

## Limitations

- This local Stage 2 run uses a 32 GiB ClickHouse container because the captured Docker VM exposes only 46.964 GiB; the 50 GiB acceptance arm is unreachable here and the local verdict is capped at Conditional.
- The 50 GiB option requires a different Docker environment with at least 54 GiB configured; no automatic memory downgrade exists.
- The OpenAlex manifests publish byte lengths and record counts but no content checksum; verification checks size and Parquet footer row counts and does not claim cryptographic object integrity.
- The Works samples are stratified by updated_date and are not a population-representative sample.
- Local Apple Silicon and local SSD latency is not extrapolated to an Alliance x86 VM with network-backed storage.
- The 50 GiB and Alliance performance envelopes remain unvalidated.
- stage2_small: the canonical Authors snapshot leaves 8133 of 3852081 Work-author bridge rows unresolved, including 8118 documented NULL-author rows and 0 documented deleted-author rows. The ordinary unresolved count is 15 of 3843963 (coverage 0.9999960978; blocking floor 0.999000). Raw links are preserved; use LEFT JOIN when unmatched authorships matter.
- stage2_medium: the canonical Authors snapshot leaves 33354 of 16075482 Work-author bridge rows unresolved, including 33089 documented NULL-author rows and 0 documented deleted-author rows. The ordinary unresolved count is 265 of 16042393 (coverage 0.9999834813; blocking floor 0.999000). Raw links are preserved; use LEFT JOIN when unmatched authorships matter.
- stage2_large: the canonical Authors snapshot leaves 98331 of 51816498 Work-author bridge rows unresolved, including 93593 documented NULL-author rows and 0 documented deleted-author rows. The ordinary unresolved count is 4738 of 51722905 (coverage 0.9999083965; blocking floor 0.999000). Raw links are preserved; use LEFT JOIN when unmatched authorships matter.
