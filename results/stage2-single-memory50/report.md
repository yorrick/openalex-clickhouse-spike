# OpenAlex ClickHouse validation — stage2-single-memory50

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
      "docker_cpus": 16,
      "docker_memory_bytes": 58866008064,
      "memory_bytes": 53687091200,
      "nano_cpus": 16000000000
    }
  },
  "inputs": {
    "complete_authors_bytes": 52769910496,
    "maximum_raw_input_bytes": 98301763421,
    "run_identity": {
      "config_sha256": "f30f5dc8ff0d754e60a9bddb803e8d91d249e262ce077766939744e13853e818",
      "download_state_sha256": "c01aa4ecf6f9b005eb14120b6de797a3e70a2c727a5e15254b6f6a8ef11a939e",
      "execution": {
        "cpus": 16,
        "maximum_seconds": 18000,
        "query_threads": 8,
        "workers": 1
      },
      "identity_version": 2,
      "memory_gib": 50,
      "rendered_sql_sha256": {
        "00_schema.sql": "9abf21c8971148d085286b5843692c1162979c331bad0bde1fce2d25d869c38d",
        "11_load_complete_authors.sql": "078e414f40660af709f654319fbebf49c6f142ab9ffd78912c0772dc97d8abd1",
        "12_load_small_dimensions.sql": "36dd9d7e91175b8f76752b6795dbbbdd59e91279d94e2abd70bd2ed6b563f6f7",
        "30_reverse_projection.sql": "72a693e47a633dcd6168b653d14c1b49dc594f54f349e669752e41ccab6bdd53",
        "stage2_large/05_raw_evidence.sql": "093f45e5f4da6e10fdc41cd301d1c2822866d11da167f74d1c753c8e1e84bbf5",
        "stage2_large/20_load_works.sql": "69cc30b79550c5a9c309215f88ac37164a9a4cccfced28b9763e655fa54f7aa4",
        "stage2_medium/05_raw_evidence.sql": "486472a3a3a3ec5a2b11d965c4933a6bce4c1bd35dbdb31fe2d694f1c8d40e5a",
        "stage2_medium/20_load_works.sql": "147ec813dc99b292136895b71dec70cd070706272e65b10f7dbad107e7a98643",
        "stage2_small/05_raw_evidence.sql": "797a7ccfaecba47b213e1664e925a39e284aeed47a89b71106934db9f0950681",
        "stage2_small/20_load_works.sql": "3ec547782549486fcfd2b08ec325e3534ed5033f51a3312d78928eceea185733"
      },
      "run_id": "stage2-single-memory50",
      "selection_sha256": "ccc7b5c51f04bd5972e6fb513f15157c13a79300be5fc5c36696aebbf56026b1",
      "sha256": "97497223d2bb1ec6039d7ddc86012f94984fe07f57241535cc1835d3f3e8b6d4",
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
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.works) AS works, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author) AS authors, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution) AS institutions, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_topic) AS topics, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.citation_edge) AS citations",
        "sql_sha256": "4a16d5ba6cf2ad0fe67c9bcd487929188cc94de7c6a78fb866e902311308a7a2"
      },
      {
        "name": "referential_coverage",
        "result_row_count": 1,
        "result_sha256": "97a87bcbd1e7199e574988b6c7ebc35e1cb86ab5bc2e171e387b43c4013534fe",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.works w ON wa.work_id=w.work_id) AS missing_works_for_authors, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author) AS author_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id) AS missing_authors, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id) AS distinct_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id) AS works_with_missing_authors, if(author_bridge_rows = 0, 1., 1 - missing_authors / author_bridge_rows) AS author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author WHERE author_id=9999999999) AS null_author_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author WHERE author_id=5317838346) AS deleted_author_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author WHERE author_id NOT IN (9999999999,5317838346)) AS ordinary_authorship_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS ordinary_missing_author_rows, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS distinct_ordinary_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS works_with_ordinary_missing_authors, if(ordinary_authorship_rows = 0, 1., 1 - ordinary_missing_author_rows / ordinary_authorship_rows) AS ordinary_author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution) AS institution_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) AS missing_institutions, (SELECT uniqExact(wi.institution_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) AS distinct_missing_institution_ids, (SELECT uniqExact(wi.work_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) AS works_with_missing_institutions, (SELECT uniqExact(wi.author_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) AS authors_with_missing_institutions, if(institution_bridge_rows = 0, 1., (institution_bridge_rows - missing_institutions) / institution_bridge_rows) AS institution_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_topic) AS topic_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.topics t ON wt.topic_id=t.topic_id) AS missing_topics, (SELECT uniqExact(wt.topic_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.topics t ON wt.topic_id=t.topic_id) AS distinct_missing_topic_ids, if(topic_bridge_rows = 0, 1., (topic_bridge_rows - missing_topics) / topic_bridge_rows) AS topic_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.citation_edge) AS citation_edges, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.citation_edge ce INNER JOIN openalex_stage2_stage2_single_memory50_8c853751.works w ON ce.cited_work_id=w.work_id) AS retained_cited_edges, if(citation_edges = 0, 1., retained_cited_edges / citation_edges) AS citation_retention_ratio",
        "sql_sha256": "4013055c9d577e87b9577182261d34953d6910d6be0eb77004881e96f1aa74a9"
      },
      {
        "name": "missing_author_sample",
        "result_row_count": 25,
        "result_sha256": "44359b4810798de7ec48cf6afb714bab06c06352e3a0b1b9d5ddd4284d670dbe",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wa.author_id FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id) SELECT openalex_numeric_id(authorship.author.id) AS author_id, multiIf(author_id=9999999999, 'null_author', author_id=5317838346, 'deleted_author', 'ordinary') AS classification, arraySlice(arraySort(groupUniqArray(ifNull(authorship.author.display_name, ''))), 1, 5) AS display_names, count() AS raw_bridge_rows FROM file('tiers/stage2_large/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship WHERE openalex_numeric_id(authorship.author.id) IN missing_ids GROUP BY author_id ORDER BY raw_bridge_rows DESC, author_id LIMIT 25",
        "sql_sha256": "50d0f97c002d923856e91d70bc1462966c5ce2489f06088930aea8cdbaf088ca"
      },
      {
        "name": "missing_institution_sample",
        "result_row_count": 25,
        "result_sha256": "0a5d7a24775cc990e0818eb12f1d49eedfbd8ffa2d44d159193ecceb3427c05a",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wi.institution_id FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) SELECT openalex_numeric_id(raw_institution.id) AS institution_id, any(raw_institution.display_name) AS display_name, count() AS raw_bridge_rows FROM file('tiers/stage2_large/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship ARRAY JOIN authorship.institutions AS raw_institution WHERE openalex_numeric_id(raw_institution.id) IN missing_ids GROUP BY institution_id ORDER BY raw_bridge_rows DESC, institution_id LIMIT 25",
        "sql_sha256": "37bbc299e4441ab197740058e1acbe8c8ad64979b2a8fda93ba01de973b31ae1"
      },
      {
        "name": "works_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "eec0816fb4eaeb19b8e4f555e3bcc79a63a63336b547593e4c25222d510d205e",
        "sql": "SELECT count() AS rows, uniqExact(work_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.works",
        "sql_sha256": "87f300723b8f712795f9e168364358881b3056c30106060c451729af2a85cb07"
      },
      {
        "name": "authors_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "ad147b0c2afdbf81139c75c21696b85568b9bd6db2c30818e5fe0d962e8a0170",
        "sql": "SELECT count() AS rows, uniqExact(author_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.authors",
        "sql_sha256": "f4e81af06962175bfa0a6375542ce655f05204b1e2f85da9b22a6d985210aeba"
      },
      {
        "name": "institutions_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "1d729a2ea001d72722af893931308d2a7ffb55562e2a5a3c33945a1cc15f9c47",
        "sql": "SELECT count() AS rows, uniqExact(institution_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.institutions",
        "sql_sha256": "403adedc2d6573955d17b157ba75ea88d5b7bc1ae87a326307c6410f7ef15ce8"
      },
      {
        "name": "sources_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "8515fa4a030ad72ca441f50ae103ac1b7701fb65366d5de9dab09a297ce71e9f",
        "sql": "SELECT count() AS rows, uniqExact(source_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.sources",
        "sql_sha256": "73f3da2ae4fe7e24175800c29ff5c11ab932d48f91c541f731eda2fb5ad54ded"
      },
      {
        "name": "topics_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "83708a811c93190b16a1b7dbe7033261c7a31e9cc7d70ade69ae253c50e5ac75",
        "sql": "SELECT count() AS rows, uniqExact(topic_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.topics",
        "sql_sha256": "d42428a72995cc7c47963524410f7ae00a0ec82ceecd3829910945c2cdee4ffa"
      },
      {
        "name": "year_type_topic_xpac_distribution",
        "result_row_count": 2201659,
        "result_sha256": "687cd62516f49aa16089bac525ce076838eeb289cadba49f0bf4c99b9192028f",
        "sql": "SELECT publication_year, work_type, primary_topic_id, is_xpac, count() AS works FROM openalex_stage2_stage2_single_memory50_8c853751.works GROUP BY ALL ORDER BY ALL",
        "sql_sha256": "beb4227733d3d93d1b6558c20472fd360b3a89bd0c3e80bc3569f42468dffb31"
      },
      {
        "name": "authorships_per_work",
        "result_row_count": 843,
        "result_sha256": "6265ea4756058c8ed86bfe5c3b998dec58901617cbb497a620400b6f1d78d37a",
        "sql": "SELECT authorships, count() AS works FROM (SELECT work_id, count() AS authorships FROM openalex_stage2_stage2_single_memory50_8c853751.work_author GROUP BY work_id) GROUP BY authorships ORDER BY authorships",
        "sql_sha256": "b5c0646fc07620da44d724734998963267022fbbb930c786337323c370a576d9"
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
      "20_load_works.sql": "69cc30b79550c5a9c309215f88ac37164a9a4cccfced28b9763e655fa54f7aa4"
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
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.works) AS works, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author) AS authors, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution) AS institutions, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_topic) AS topics, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.citation_edge) AS citations",
        "sql_sha256": "4a16d5ba6cf2ad0fe67c9bcd487929188cc94de7c6a78fb866e902311308a7a2"
      },
      {
        "name": "referential_coverage",
        "result_row_count": 1,
        "result_sha256": "9bfc14c04fcf4b2beb8ad257b9bc2d24f9e5b9f486bac539bfa8a33728e53a50",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.works w ON wa.work_id=w.work_id) AS missing_works_for_authors, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author) AS author_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id) AS missing_authors, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id) AS distinct_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id) AS works_with_missing_authors, if(author_bridge_rows = 0, 1., 1 - missing_authors / author_bridge_rows) AS author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author WHERE author_id=9999999999) AS null_author_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author WHERE author_id=5317838346) AS deleted_author_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author WHERE author_id NOT IN (9999999999,5317838346)) AS ordinary_authorship_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS ordinary_missing_author_rows, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS distinct_ordinary_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS works_with_ordinary_missing_authors, if(ordinary_authorship_rows = 0, 1., 1 - ordinary_missing_author_rows / ordinary_authorship_rows) AS ordinary_author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution) AS institution_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) AS missing_institutions, (SELECT uniqExact(wi.institution_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) AS distinct_missing_institution_ids, (SELECT uniqExact(wi.work_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) AS works_with_missing_institutions, (SELECT uniqExact(wi.author_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) AS authors_with_missing_institutions, if(institution_bridge_rows = 0, 1., (institution_bridge_rows - missing_institutions) / institution_bridge_rows) AS institution_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_topic) AS topic_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.topics t ON wt.topic_id=t.topic_id) AS missing_topics, (SELECT uniqExact(wt.topic_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.topics t ON wt.topic_id=t.topic_id) AS distinct_missing_topic_ids, if(topic_bridge_rows = 0, 1., (topic_bridge_rows - missing_topics) / topic_bridge_rows) AS topic_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.citation_edge) AS citation_edges, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.citation_edge ce INNER JOIN openalex_stage2_stage2_single_memory50_8c853751.works w ON ce.cited_work_id=w.work_id) AS retained_cited_edges, if(citation_edges = 0, 1., retained_cited_edges / citation_edges) AS citation_retention_ratio",
        "sql_sha256": "4013055c9d577e87b9577182261d34953d6910d6be0eb77004881e96f1aa74a9"
      },
      {
        "name": "missing_author_sample",
        "result_row_count": 25,
        "result_sha256": "2029b08cef3cc2b317e2e92a98c1c91cfbed1f75ef27fafca4b6a895f7c9fc95",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wa.author_id FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id) SELECT openalex_numeric_id(authorship.author.id) AS author_id, multiIf(author_id=9999999999, 'null_author', author_id=5317838346, 'deleted_author', 'ordinary') AS classification, arraySlice(arraySort(groupUniqArray(ifNull(authorship.author.display_name, ''))), 1, 5) AS display_names, count() AS raw_bridge_rows FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship WHERE openalex_numeric_id(authorship.author.id) IN missing_ids GROUP BY author_id ORDER BY raw_bridge_rows DESC, author_id LIMIT 25",
        "sql_sha256": "68a567414938c577b902a43fc341c821092896d21a2dc56361403bb99a0f7088"
      },
      {
        "name": "missing_institution_sample",
        "result_row_count": 25,
        "result_sha256": "041d556c79b9cc31f860bd11a2eb21e1f96d47e8e9ce9c80b50b2f84fd9f03c5",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wi.institution_id FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) SELECT openalex_numeric_id(raw_institution.id) AS institution_id, any(raw_institution.display_name) AS display_name, count() AS raw_bridge_rows FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship ARRAY JOIN authorship.institutions AS raw_institution WHERE openalex_numeric_id(raw_institution.id) IN missing_ids GROUP BY institution_id ORDER BY raw_bridge_rows DESC, institution_id LIMIT 25",
        "sql_sha256": "e7b97cba3a3f461394f1db47b3b71f4f4f91017cf129ea60f405c207c94e95c6"
      },
      {
        "name": "works_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "56aabad587204e1a393c30baf149217c0ee158c3b8434f32e4eba7ae0aae34cf",
        "sql": "SELECT count() AS rows, uniqExact(work_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.works",
        "sql_sha256": "87f300723b8f712795f9e168364358881b3056c30106060c451729af2a85cb07"
      },
      {
        "name": "authors_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "ad147b0c2afdbf81139c75c21696b85568b9bd6db2c30818e5fe0d962e8a0170",
        "sql": "SELECT count() AS rows, uniqExact(author_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.authors",
        "sql_sha256": "f4e81af06962175bfa0a6375542ce655f05204b1e2f85da9b22a6d985210aeba"
      },
      {
        "name": "institutions_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "1d729a2ea001d72722af893931308d2a7ffb55562e2a5a3c33945a1cc15f9c47",
        "sql": "SELECT count() AS rows, uniqExact(institution_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.institutions",
        "sql_sha256": "403adedc2d6573955d17b157ba75ea88d5b7bc1ae87a326307c6410f7ef15ce8"
      },
      {
        "name": "sources_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "8515fa4a030ad72ca441f50ae103ac1b7701fb65366d5de9dab09a297ce71e9f",
        "sql": "SELECT count() AS rows, uniqExact(source_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.sources",
        "sql_sha256": "73f3da2ae4fe7e24175800c29ff5c11ab932d48f91c541f731eda2fb5ad54ded"
      },
      {
        "name": "topics_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "83708a811c93190b16a1b7dbe7033261c7a31e9cc7d70ade69ae253c50e5ac75",
        "sql": "SELECT count() AS rows, uniqExact(topic_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.topics",
        "sql_sha256": "d42428a72995cc7c47963524410f7ae00a0ec82ceecd3829910945c2cdee4ffa"
      },
      {
        "name": "year_type_topic_xpac_distribution",
        "result_row_count": 1307378,
        "result_sha256": "9fd1a41a5f5bc8119582c700239d950531afec5124792c9998806df498e7da42",
        "sql": "SELECT publication_year, work_type, primary_topic_id, is_xpac, count() AS works FROM openalex_stage2_stage2_single_memory50_8c853751.works GROUP BY ALL ORDER BY ALL",
        "sql_sha256": "beb4227733d3d93d1b6558c20472fd360b3a89bd0c3e80bc3569f42468dffb31"
      },
      {
        "name": "authorships_per_work",
        "result_row_count": 447,
        "result_sha256": "2bc843d8da3f9998d26c7d558b7c8464e08af5a43f8e0128f60d3aa4c3f77d9e",
        "sql": "SELECT authorships, count() AS works FROM (SELECT work_id, count() AS authorships FROM openalex_stage2_stage2_single_memory50_8c853751.work_author GROUP BY work_id) GROUP BY authorships ORDER BY authorships",
        "sql_sha256": "b5c0646fc07620da44d724734998963267022fbbb930c786337323c370a576d9"
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
      "20_load_works.sql": "147ec813dc99b292136895b71dec70cd070706272e65b10f7dbad107e7a98643"
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
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.works) AS works, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author) AS authors, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution) AS institutions, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_topic) AS topics, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.citation_edge) AS citations",
        "sql_sha256": "4a16d5ba6cf2ad0fe67c9bcd487929188cc94de7c6a78fb866e902311308a7a2"
      },
      {
        "name": "referential_coverage",
        "result_row_count": 1,
        "result_sha256": "aaacea8bab04a1689cbd1580515b55fb7b21aa9a3ec549a22df8b6c55a6add54",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.works w ON wa.work_id=w.work_id) AS missing_works_for_authors, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author) AS author_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id) AS missing_authors, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id) AS distinct_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id) AS works_with_missing_authors, if(author_bridge_rows = 0, 1., 1 - missing_authors / author_bridge_rows) AS author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author WHERE author_id=9999999999) AS null_author_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author WHERE author_id=5317838346) AS deleted_author_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author WHERE author_id NOT IN (9999999999,5317838346)) AS ordinary_authorship_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS ordinary_missing_author_rows, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS distinct_ordinary_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS works_with_ordinary_missing_authors, if(ordinary_authorship_rows = 0, 1., 1 - ordinary_missing_author_rows / ordinary_authorship_rows) AS ordinary_author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution) AS institution_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) AS missing_institutions, (SELECT uniqExact(wi.institution_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) AS distinct_missing_institution_ids, (SELECT uniqExact(wi.work_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) AS works_with_missing_institutions, (SELECT uniqExact(wi.author_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) AS authors_with_missing_institutions, if(institution_bridge_rows = 0, 1., (institution_bridge_rows - missing_institutions) / institution_bridge_rows) AS institution_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_topic) AS topic_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.topics t ON wt.topic_id=t.topic_id) AS missing_topics, (SELECT uniqExact(wt.topic_id) FROM openalex_stage2_stage2_single_memory50_8c853751.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.topics t ON wt.topic_id=t.topic_id) AS distinct_missing_topic_ids, if(topic_bridge_rows = 0, 1., (topic_bridge_rows - missing_topics) / topic_bridge_rows) AS topic_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.citation_edge) AS citation_edges, (SELECT count() FROM openalex_stage2_stage2_single_memory50_8c853751.citation_edge ce INNER JOIN openalex_stage2_stage2_single_memory50_8c853751.works w ON ce.cited_work_id=w.work_id) AS retained_cited_edges, if(citation_edges = 0, 1., retained_cited_edges / citation_edges) AS citation_retention_ratio",
        "sql_sha256": "4013055c9d577e87b9577182261d34953d6910d6be0eb77004881e96f1aa74a9"
      },
      {
        "name": "missing_author_sample",
        "result_row_count": 14,
        "result_sha256": "99a76bcebd2eb596aad11499de36d0f0433fdd046319d0bec9237a41f9f28082",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wa.author_id FROM openalex_stage2_stage2_single_memory50_8c853751.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.authors a ON wa.author_id=a.author_id) SELECT openalex_numeric_id(authorship.author.id) AS author_id, multiIf(author_id=9999999999, 'null_author', author_id=5317838346, 'deleted_author', 'ordinary') AS classification, arraySlice(arraySort(groupUniqArray(ifNull(authorship.author.display_name, ''))), 1, 5) AS display_names, count() AS raw_bridge_rows FROM file('tiers/stage2_small/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship WHERE openalex_numeric_id(authorship.author.id) IN missing_ids GROUP BY author_id ORDER BY raw_bridge_rows DESC, author_id LIMIT 25",
        "sql_sha256": "4f3b86bda207ccc1f5e1398fa5be0920c5bed282fd89b8a39ad58ca96431a128"
      },
      {
        "name": "missing_institution_sample",
        "result_row_count": 25,
        "result_sha256": "e76891d77558501c47c0f69c20680983202e0d65482fb85bfcbd131b4f66f365",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wi.institution_id FROM openalex_stage2_stage2_single_memory50_8c853751.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_single_memory50_8c853751.institutions i ON wi.institution_id=i.institution_id) SELECT openalex_numeric_id(raw_institution.id) AS institution_id, any(raw_institution.display_name) AS display_name, count() AS raw_bridge_rows FROM file('tiers/stage2_small/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship ARRAY JOIN authorship.institutions AS raw_institution WHERE openalex_numeric_id(raw_institution.id) IN missing_ids GROUP BY institution_id ORDER BY raw_bridge_rows DESC, institution_id LIMIT 25",
        "sql_sha256": "5da6fd6a054fe8ae8f7a4138a308639316701961c370daa7c471d5268786de2b"
      },
      {
        "name": "works_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "74a4b54bd6c6fe3b72ff60e9d31fff2d02e1622bd0a05fa63ef21325131ac1b5",
        "sql": "SELECT count() AS rows, uniqExact(work_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.works",
        "sql_sha256": "87f300723b8f712795f9e168364358881b3056c30106060c451729af2a85cb07"
      },
      {
        "name": "authors_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "ad147b0c2afdbf81139c75c21696b85568b9bd6db2c30818e5fe0d962e8a0170",
        "sql": "SELECT count() AS rows, uniqExact(author_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.authors",
        "sql_sha256": "f4e81af06962175bfa0a6375542ce655f05204b1e2f85da9b22a6d985210aeba"
      },
      {
        "name": "institutions_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "1d729a2ea001d72722af893931308d2a7ffb55562e2a5a3c33945a1cc15f9c47",
        "sql": "SELECT count() AS rows, uniqExact(institution_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.institutions",
        "sql_sha256": "403adedc2d6573955d17b157ba75ea88d5b7bc1ae87a326307c6410f7ef15ce8"
      },
      {
        "name": "sources_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "8515fa4a030ad72ca441f50ae103ac1b7701fb65366d5de9dab09a297ce71e9f",
        "sql": "SELECT count() AS rows, uniqExact(source_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.sources",
        "sql_sha256": "73f3da2ae4fe7e24175800c29ff5c11ab932d48f91c541f731eda2fb5ad54ded"
      },
      {
        "name": "topics_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "83708a811c93190b16a1b7dbe7033261c7a31e9cc7d70ade69ae253c50e5ac75",
        "sql": "SELECT count() AS rows, uniqExact(topic_id) AS unique_ids FROM openalex_stage2_stage2_single_memory50_8c853751.topics",
        "sql_sha256": "d42428a72995cc7c47963524410f7ae00a0ec82ceecd3829910945c2cdee4ffa"
      },
      {
        "name": "year_type_topic_xpac_distribution",
        "result_row_count": 492399,
        "result_sha256": "89b42e728db3c8983e10ef0e5324c51deb698afea5daa05dcefcf53b0917024e",
        "sql": "SELECT publication_year, work_type, primary_topic_id, is_xpac, count() AS works FROM openalex_stage2_stage2_single_memory50_8c853751.works GROUP BY ALL ORDER BY ALL",
        "sql_sha256": "beb4227733d3d93d1b6558c20472fd360b3a89bd0c3e80bc3569f42468dffb31"
      },
      {
        "name": "authorships_per_work",
        "result_row_count": 200,
        "result_sha256": "8c704127e6d040ac4779ce338b625f61ecd0f9a7faee500ee1f59850b8dc3b38",
        "sql": "SELECT authorships, count() AS works FROM (SELECT work_id, count() AS authorships FROM openalex_stage2_stage2_single_memory50_8c853751.work_author GROUP BY work_id) GROUP BY authorships ORDER BY authorships",
        "sql_sha256": "b5c0646fc07620da44d724734998963267022fbbb930c786337323c370a576d9"
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
      "20_load_works.sql": "3ec547782549486fcfd2b08ec325e3534ed5033f51a3312d78928eceea185733"
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
          "maximum_seconds": 408.016,
          "median_seconds": 39.557,
          "p95_seconds": 306.858,
          "peak_memory_bytes": 4657894160,
          "read_bytes": 375047789600,
          "read_rows": 20522546850,
          "spill_bytes": 0
        },
        "one_hop": {
          "count": 50,
          "insufficient_sample": false,
          "maximum_seconds": 0.665,
          "median_seconds": 0.017,
          "p95_seconds": 0.139,
          "peak_memory_bytes": 5734075,
          "read_bytes": 1748776264,
          "read_rows": 216880883,
          "spill_bytes": 0
        },
        "routine": {
          "count": 99,
          "insufficient_sample": false,
          "maximum_seconds": 217.084,
          "median_seconds": 5.144,
          "p95_seconds": 169.067,
          "peak_memory_bytes": 5689693892,
          "read_bytes": 122101866093,
          "read_rows": 11824834213,
          "spill_bytes": 0
        }
      },
      "execution": {
        "cpus": 16,
        "maximum_seconds": 18000,
        "query_threads": 8,
        "workers": 1
      },
      "first_error": null,
      "forced_verdict": null,
      "server_restarted": false,
      "verdict_cap": "pass"
    },
    "stage2_medium": {
      "classes": {
        "join": {
          "count": 150,
          "insufficient_sample": false,
          "maximum_seconds": 33.556,
          "median_seconds": 3.398,
          "p95_seconds": 14.532,
          "peak_memory_bytes": 4487476675,
          "read_bytes": 227401335000,
          "read_rows": 10624296150,
          "spill_bytes": 0
        },
        "one_hop": {
          "count": 50,
          "insufficient_sample": false,
          "maximum_seconds": 0.092,
          "median_seconds": 0.007,
          "p95_seconds": 0.011,
          "peak_memory_bytes": 2175510,
          "read_bytes": 574721072,
          "read_rows": 71235184,
          "spill_bytes": 0
        },
        "routine": {
          "count": 99,
          "insufficient_sample": false,
          "maximum_seconds": 4.085,
          "median_seconds": 0.073,
          "p95_seconds": 1.984,
          "peak_memory_bytes": 4447952054,
          "read_bytes": 40987135276,
          "read_rows": 3955869866,
          "spill_bytes": 0
        }
      },
      "execution": {
        "cpus": 16,
        "maximum_seconds": 18000,
        "query_threads": 8,
        "workers": 1
      },
      "first_error": null,
      "forced_verdict": null,
      "server_restarted": false,
      "verdict_cap": "pass"
    },
    "stage2_small": {
      "classes": {
        "join": {
          "count": 150,
          "insufficient_sample": false,
          "maximum_seconds": 1.712,
          "median_seconds": 0.391,
          "p95_seconds": 1.208,
          "peak_memory_bytes": 2160413299,
          "read_bytes": 172574035100,
          "read_rows": 6934116600,
          "spill_bytes": 0
        },
        "one_hop": {
          "count": 50,
          "insufficient_sample": false,
          "maximum_seconds": 0.026,
          "median_seconds": 0.003,
          "p95_seconds": 0.005,
          "peak_memory_bytes": 1147204,
          "read_bytes": 136132864,
          "read_rows": 16929608,
          "spill_bytes": 0
        },
        "routine": {
          "count": 99,
          "insufficient_sample": false,
          "maximum_seconds": 0.441,
          "median_seconds": 0.035,
          "p95_seconds": 0.305,
          "peak_memory_bytes": 1109731847,
          "read_bytes": 8838440224,
          "read_rows": 849016884,
          "spill_bytes": 0
        }
      },
      "execution": {
        "cpus": 16,
        "maximum_seconds": 18000,
        "query_threads": 8,
        "workers": 1
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
        "elapsed_seconds": 0.798,
        "gating": true,
        "peak_memory_bytes": 108974778,
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
        "elapsed_seconds": 0.81,
        "gating": true,
        "peak_memory_bytes": 108813004,
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
        "elapsed_seconds": 0.883,
        "gating": true,
        "peak_memory_bytes": 107768386,
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
        "elapsed_seconds": 0.736,
        "gating": true,
        "peak_memory_bytes": 108965153,
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
        "elapsed_seconds": 3.187,
        "gating": true,
        "peak_memory_bytes": 108603333,
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
        "elapsed_seconds": 0.787,
        "gating": true,
        "peak_memory_bytes": 108217078,
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
        "elapsed_seconds": 176.681,
        "gating": true,
        "peak_memory_bytes": 4335997285,
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
        "elapsed_seconds": 70.703,
        "gating": true,
        "peak_memory_bytes": 4355967512,
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
        "elapsed_seconds": 68.093,
        "gating": true,
        "peak_memory_bytes": 4327940318,
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
        "elapsed_seconds": 69.984,
        "gating": true,
        "peak_memory_bytes": 4322317209,
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
        "elapsed_seconds": 70.816,
        "gating": true,
        "peak_memory_bytes": 4322233827,
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
        "elapsed_seconds": 125.545,
        "gating": true,
        "peak_memory_bytes": 4354876461,
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
        "elapsed_seconds": 34.557,
        "gating": true,
        "peak_memory_bytes": 4460730458,
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
        "elapsed_seconds": 10.123,
        "gating": true,
        "peak_memory_bytes": 4462447248,
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
        "elapsed_seconds": 10.036,
        "gating": true,
        "peak_memory_bytes": 4461856765,
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
        "elapsed_seconds": 10.343,
        "gating": true,
        "peak_memory_bytes": 4365757249,
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
        "elapsed_seconds": 10.485,
        "gating": true,
        "peak_memory_bytes": 4383522085,
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
        "elapsed_seconds": 10.767,
        "gating": true,
        "peak_memory_bytes": 4398673592,
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
        "elapsed_seconds": 35.372,
        "gating": true,
        "peak_memory_bytes": 4762497752,
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
        "elapsed_seconds": 34.501,
        "gating": true,
        "peak_memory_bytes": 4785431669,
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
        "elapsed_seconds": 36.263,
        "gating": true,
        "peak_memory_bytes": 4806517437,
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
        "elapsed_seconds": 39.222,
        "gating": true,
        "peak_memory_bytes": 4799799648,
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
        "elapsed_seconds": 18.554,
        "gating": true,
        "peak_memory_bytes": 4818731653,
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
        "elapsed_seconds": 40.726,
        "gating": true,
        "peak_memory_bytes": 4808589743,
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
        "elapsed_seconds": 7.58,
        "gating": true,
        "peak_memory_bytes": 5796584,
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
        "elapsed_seconds": 1.687,
        "gating": true,
        "peak_memory_bytes": 5770803,
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
        "elapsed_seconds": 0.249,
        "gating": true,
        "peak_memory_bytes": 5854576,
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
        "peak_memory_bytes": 317360,
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
        "elapsed_seconds": 0.013,
        "gating": true,
        "peak_memory_bytes": 449147,
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
        "peak_memory_bytes": 811384,
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
        "elapsed_seconds": 0.028,
        "gating": false,
        "peak_memory_bytes": 550272,
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
        "elapsed_seconds": 0.452,
        "gating": false,
        "peak_memory_bytes": 10976340,
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
        "elapsed_seconds": 0.306,
        "gating": false,
        "peak_memory_bytes": 18314802,
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
        "elapsed_seconds": 0.005,
        "gating": false,
        "peak_memory_bytes": 512960,
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
        "elapsed_seconds": 0.313,
        "gating": false,
        "peak_memory_bytes": 10289400,
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
        "elapsed_seconds": 0.317,
        "gating": false,
        "peak_memory_bytes": 18095154,
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
        "elapsed_seconds": 4.153,
        "gating": true,
        "peak_memory_bytes": 5906789776,
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
        "elapsed_seconds": 4.124,
        "gating": true,
        "peak_memory_bytes": 5856192890,
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
        "elapsed_seconds": 4.161,
        "gating": true,
        "peak_memory_bytes": 5683753963,
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
        "elapsed_seconds": 4.256,
        "gating": true,
        "peak_memory_bytes": 5985212987,
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
        "elapsed_seconds": 4.301,
        "gating": true,
        "peak_memory_bytes": 5817180211,
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
        "elapsed_seconds": 4.63,
        "gating": true,
        "peak_memory_bytes": 5477995849,
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
        "elapsed_seconds": 0.054,
        "gating": true,
        "peak_memory_bytes": 107290917,
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
        "elapsed_seconds": 0.027,
        "gating": true,
        "peak_memory_bytes": 107797114,
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
        "elapsed_seconds": 0.027,
        "gating": true,
        "peak_memory_bytes": 107925668,
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
        "elapsed_seconds": 0.027,
        "gating": true,
        "peak_memory_bytes": 107795546,
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
        "elapsed_seconds": 0.026,
        "gating": true,
        "peak_memory_bytes": 107901571,
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
        "elapsed_seconds": 0.028,
        "gating": true,
        "peak_memory_bytes": 107869439,
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
        "elapsed_seconds": 9.554,
        "gating": true,
        "peak_memory_bytes": 2969017748,
        "query_class": "join",
        "query_id": "13595f55-8ce6-5f96-9afd-a4a8889d126a",
        "query_name": "q02",
        "read_bytes": 496748658,
        "read_rows": 31771253,
        "result_rows": 579800,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 10.403,
        "gating": true,
        "peak_memory_bytes": 2960420467,
        "query_class": "join",
        "query_id": "a2848046-3ec2-5022-963e-ecd8f76e25e6",
        "query_name": "q02",
        "read_bytes": 496748658,
        "read_rows": 31771253,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 10.7,
        "gating": true,
        "peak_memory_bytes": 2936659839,
        "query_class": "join",
        "query_id": "5504b261-1dca-5b3c-a586-47a9e9403c20",
        "query_name": "q02",
        "read_bytes": 496748658,
        "read_rows": 31771253,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 10.281,
        "gating": true,
        "peak_memory_bytes": 2961149943,
        "query_class": "join",
        "query_id": "edd03e6a-5f6b-5a3c-9c5b-bc50f3eddaad",
        "query_name": "q02",
        "read_bytes": 496748658,
        "read_rows": 31771253,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 10.556,
        "gating": true,
        "peak_memory_bytes": 2954832696,
        "query_class": "join",
        "query_id": "bfad4687-cb42-5ffe-bbec-e399dc66ffac",
        "query_name": "q02",
        "read_bytes": 496748658,
        "read_rows": 31771253,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 11.505,
        "gating": true,
        "peak_memory_bytes": 2948592212,
        "query_class": "join",
        "query_id": "c63b7a6c-1bb7-5a2d-8f4b-edc4eb13fe71",
        "query_name": "q02",
        "read_bytes": 496748658,
        "read_rows": 31771253,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 3.043,
        "gating": true,
        "peak_memory_bytes": 4412407553,
        "query_class": "join",
        "query_id": "55a2bf14-7bc6-50bb-b8f8-e7afc7b5a6d8",
        "query_name": "q03",
        "read_bytes": 3534690631,
        "read_rows": 145314875,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 3.421,
        "gating": true,
        "peak_memory_bytes": 4482684474,
        "query_class": "join",
        "query_id": "68b45e30-86bb-5487-9691-09331c63a648",
        "query_name": "q03",
        "read_bytes": 3534690631,
        "read_rows": 145314875,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 3.379,
        "gating": true,
        "peak_memory_bytes": 4439393099,
        "query_class": "join",
        "query_id": "c3ea97aa-7c10-5851-805d-648e39c76f4d",
        "query_name": "q03",
        "read_bytes": 3534690631,
        "read_rows": 145314875,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 3.425,
        "gating": true,
        "peak_memory_bytes": 4456309915,
        "query_class": "join",
        "query_id": "02ca305d-ad37-5cb1-a79a-a037ed6dc1df",
        "query_name": "q03",
        "read_bytes": 3534690631,
        "read_rows": 145314875,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 3.189,
        "gating": true,
        "peak_memory_bytes": 4358923840,
        "query_class": "join",
        "query_id": "5e44ed1a-1a6c-53c4-963f-15b1773e443c",
        "query_name": "q03",
        "read_bytes": 3534690631,
        "read_rows": 145314875,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 3.39,
        "gating": true,
        "peak_memory_bytes": 4355385915,
        "query_class": "join",
        "query_id": "940ad897-60ba-5c49-9760-e4c1df1d7253",
        "query_name": "q03",
        "read_bytes": 3534690631,
        "read_rows": 145314875,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "seed_work_id": null,
        "spill_bytes": 0
      },
      {
        "elapsed_seconds": 2.624,
        "gating": true,
        "peak_memory_bytes": 2205928394,
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
        "elapsed_seconds": 2.499,
        "gating": true,
        "peak_memory_bytes": 2203038776,
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
        "elapsed_seconds": 2.599,
        "gating": true,
        "peak_memory_bytes": 2206453475,
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
        "elapsed_seconds": 2.59,
        "gating": true,
        "peak_memory_bytes": 2202361038,
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
        "elapsed_seconds": 2.579,
        "gating": true,
        "peak_memory_bytes": 2202276712,
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
        "elapsed_seconds": 2.546,
        "gating": true,
        "peak_memory_bytes": 2209744861,
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
        "peak_memory_bytes": 2169968,
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
        "elapsed_seconds": 0.083,
        "gating": true,
        "peak_memory_bytes": 2168214,
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
        "elapsed_seconds": 0.088,
        "gating": true,
        "peak_memory_bytes": 2415561,
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
        "peak_memory_bytes": 317168,
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
        "peak_memory_bytes": 355222,
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
        "peak_memory_bytes": 435510,
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
        "peak_memory_bytes": 491456,
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
        "peak_memory_bytes": 6513054,
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
        "elapsed_seconds": 0.12,
        "gating": false,
        "peak_memory_bytes": 11603486,
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
        "peak_memory_bytes": 471592,
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
        "elapsed_seconds": 0.097,
        "gating": false,
        "peak_memory_bytes": 6205508,
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
        "elapsed_seconds": 0.098,
        "gating": false,
        "peak_memory_bytes": 12465510,
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
        "elapsed_seconds": 1.535,
        "gating": true,
        "peak_memory_bytes": 5825901269,
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
        "elapsed_seconds": 1.643,
        "gating": true,
        "peak_memory_bytes": 5877486629,
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
        "elapsed_seconds": 1.607,
        "gating": true,
        "peak_memory_bytes": 5534637037,
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
        "elapsed_seconds": 1.54,
        "gating": true,
        "peak_memory_bytes": 5804395141,
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
        "elapsed_seconds": 1.545,
        "gating": true,
        "peak_memory_bytes": 5512467517,
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
        "elapsed_seconds": 1.528,
        "gating": true,
        "peak_memory_bytes": 5678550741,
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
        "elapsed_seconds": 0.11,
        "gating": true,
        "peak_memory_bytes": 34724229,
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
        "elapsed_seconds": 0.049,
        "gating": true,
        "peak_memory_bytes": 39480450,
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
        "elapsed_seconds": 0.018,
        "gating": true,
        "peak_memory_bytes": 67056619,
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
        "elapsed_seconds": 0.018,
        "gating": true,
        "peak_memory_bytes": 61905244,
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
        "elapsed_seconds": 0.016,
        "gating": true,
        "peak_memory_bytes": 65580629,
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
        "elapsed_seconds": 0.018,
        "gating": true,
        "peak_memory_bytes": 72730783,
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
        "elapsed_seconds": 0.263,
        "gating": true,
        "peak_memory_bytes": 1160013748,
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
        "elapsed_seconds": 0.268,
        "gating": true,
        "peak_memory_bytes": 1123361117,
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
        "elapsed_seconds": 0.249,
        "gating": true,
        "peak_memory_bytes": 1111520921,
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
        "elapsed_seconds": 0.264,
        "gating": true,
        "peak_memory_bytes": 1123273396,
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
        "elapsed_seconds": 0.249,
        "gating": true,
        "peak_memory_bytes": 1136191235,
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
        "elapsed_seconds": 0.246,
        "gating": true,
        "peak_memory_bytes": 1121795692,
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
        "elapsed_seconds": 0.908,
        "gating": true,
        "peak_memory_bytes": 2326079565,
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
        "elapsed_seconds": 0.817,
        "gating": true,
        "peak_memory_bytes": 2120913518,
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
        "elapsed_seconds": 0.835,
        "gating": true,
        "peak_memory_bytes": 2126825005,
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
        "elapsed_seconds": 0.861,
        "gating": true,
        "peak_memory_bytes": 2139445234,
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
        "elapsed_seconds": 0.846,
        "gating": true,
        "peak_memory_bytes": 2118910458,
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
        "elapsed_seconds": 0.836,
        "gating": true,
        "peak_memory_bytes": 2139458434,
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
        "elapsed_seconds": 0.35,
        "gating": true,
        "peak_memory_bytes": 685293626,
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
        "elapsed_seconds": 0.336,
        "gating": true,
        "peak_memory_bytes": 690192729,
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
        "elapsed_seconds": 0.366,
        "gating": true,
        "peak_memory_bytes": 686078408,
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
        "elapsed_seconds": 0.354,
        "gating": true,
        "peak_memory_bytes": 679142042,
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
        "elapsed_seconds": 0.374,
        "gating": true,
        "peak_memory_bytes": 686167356,
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
        "elapsed_seconds": 0.331,
        "gating": true,
        "peak_memory_bytes": 674320648,
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
        "elapsed_seconds": 0.038,
        "gating": true,
        "peak_memory_bytes": 805512,
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
        "elapsed_seconds": 0.023,
        "gating": true,
        "peak_memory_bytes": 842572,
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
        "elapsed_seconds": 0.024,
        "gating": true,
        "peak_memory_bytes": 1002984,
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
        "peak_memory_bytes": 317168,
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
        "peak_memory_bytes": 391028,
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
        "peak_memory_bytes": 732578,
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
        "elapsed_seconds": 0.003,
        "gating": false,
        "peak_memory_bytes": 484216,
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
        "elapsed_seconds": 0.028,
        "gating": false,
        "peak_memory_bytes": 6236675,
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
        "elapsed_seconds": 0.031,
        "gating": false,
        "peak_memory_bytes": 8731519,
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
        "peak_memory_bytes": 469808,
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
        "elapsed_seconds": 0.029,
        "gating": false,
        "peak_memory_bytes": 6796390,
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
        "peak_memory_bytes": 8727759,
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
        "elapsed_seconds": 0.205,
        "gating": true,
        "peak_memory_bytes": 1611864951,
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
        "elapsed_seconds": 0.161,
        "gating": true,
        "peak_memory_bytes": 963746567,
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
        "elapsed_seconds": 0.148,
        "gating": true,
        "peak_memory_bytes": 858045203,
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
        "elapsed_seconds": 0.15,
        "gating": true,
        "peak_memory_bytes": 877899283,
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
        "elapsed_seconds": 0.162,
        "gating": true,
        "peak_memory_bytes": 958085515,
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
        "elapsed_seconds": 0.158,
        "gating": true,
        "peak_memory_bytes": 853331017,
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
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 30618020
      },
      "timestamp": 1785937800.7438028
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 256982647
      },
      "timestamp": 1785937801.9958458
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 446218742
      },
      "timestamp": 1785937803.246357
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 662434669
      },
      "timestamp": 1785937804.5151072
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 907127116
      },
      "timestamp": 1785937805.781642
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1157600516
      },
      "timestamp": 1785937807.05374
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1378418261
      },
      "timestamp": 1785937808.286319
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1591617120
      },
      "timestamp": 1785937809.572308
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1808631662
      },
      "timestamp": 1785937810.831289
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2025589926
      },
      "timestamp": 1785937812.086438
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2237004746
      },
      "timestamp": 1785937813.338728
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2448791719
      },
      "timestamp": 1785937814.583786
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2661095106
      },
      "timestamp": 1785937815.835254
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2880039719
      },
      "timestamp": 1785937817.088115
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3071835727
      },
      "timestamp": 1785937818.3278432
    },
    {
      "filesystem_bytes": 14912917504,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3288877846
      },
      "timestamp": 1785937819.565218
    },
    {
      "filesystem_bytes": 23861321728,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3400453449,
        "institutions": 4357308,
        "sources": 10677280,
        "topics": 150309
      },
      "timestamp": 1785937820.573578
    }
  ],
  "tiers": {
    "stage2_large": [
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 46678785
        },
        "timestamp": 1785943310.1526132
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 198701361
        },
        "timestamp": 1785943311.36049
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 355609191
        },
        "timestamp": 1785943312.568408
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 481497321
        },
        "timestamp": 1785943313.773602
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 658083265
        },
        "timestamp": 1785943315.074682
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 651943500
        },
        "timestamp": 1785943316.367697
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943317.661852
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943319.2632709
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943320.535923
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943321.832453
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943323.064758
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943324.278062
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943325.5551429
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 191002002,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943326.788141
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 331403546,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943328.046259
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 505795400,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943329.273159
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 646291894,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943330.533105
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 786749025,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943331.770095
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 943838720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943333.028927
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1084233525,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943334.2815418
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1224615704,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943335.54783
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1247509092,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943336.80914
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1370604907,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943338.206672
      },
      {
        "filesystem_bytes": 18153717760,
        "filesystem_vanished_directories": 1,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1510298270,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943339.476236
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1720893559,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 645382468
        },
        "timestamp": 1785943341.295684
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1657182869,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 23256794,
          "works": 645382468
        },
        "timestamp": 1785943342.608348
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1640600552,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 108203615,
          "works": 645382468
        },
        "timestamp": 1785943343.909238
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1640600552,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 189957581,
          "works": 645382468
        },
        "timestamp": 1785943345.207346
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1640600552,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 274043793,
          "works": 645382468
        },
        "timestamp": 1785943346.5164428
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1640600552,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 346077949,
          "works": 645382468
        },
        "timestamp": 1785943347.855606
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 416291706,
          "works": 645382468
        },
        "timestamp": 1785943349.165505
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 496373756,
          "works": 645382468
        },
        "timestamp": 1785943350.418357
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 491144777,
          "work_institution": 9385278,
          "works": 645382468
        },
        "timestamp": 1785943351.6879418
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 491144777,
          "work_institution": 44724624,
          "works": 645382468
        },
        "timestamp": 1785943352.935362
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 491144777,
          "work_institution": 67589264,
          "works": 645382468
        },
        "timestamp": 1785943354.214463
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 94109901,
          "works": 645382468
        },
        "timestamp": 1785943355.483535
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 117724014,
          "works": 645382468
        },
        "timestamp": 1785943356.711201
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 144873759,
          "works": 645382468
        },
        "timestamp": 1785943357.958393
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 177552710,
          "works": 645382468
        },
        "timestamp": 1785943359.220753
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 212662473,
          "works": 645382468
        },
        "timestamp": 1785943360.477957
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 244393873,
          "works": 645382468
        },
        "timestamp": 1785943361.742272
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 253443313,
          "works": 645382468
        },
        "timestamp": 1785943362.988241
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 289931475,
          "works": 645382468
        },
        "timestamp": 1785943364.223712
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 299706948,
          "work_topic": 10381009,
          "works": 645382468
        },
        "timestamp": 1785943365.4823859
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 299706948,
          "work_topic": 120251832,
          "works": 645382468
        },
        "timestamp": 1785943366.727181
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 299706948,
          "work_topic": 240231982,
          "works": 645382468
        },
        "timestamp": 1785943367.964436
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 299706948,
          "work_topic": 351530264,
          "works": 645382468
        },
        "timestamp": 1785943369.2422779
      },
      {
        "filesystem_bytes": 26976251904,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 299706948,
          "work_topic": 472191517,
          "works": 645382468
        },
        "timestamp": 1785943370.499966
      },
      {
        "filesystem_bytes": 28010790912,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 299706948,
          "work_topic": 540993555,
          "works": 645382468
        },
        "timestamp": 1785943372.5457852
      },
      {
        "filesystem_bytes": 28205154304,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 1524033369,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 453924772,
          "work_institution": 299706948,
          "work_topic": 602580060,
          "works": 645382468
        },
        "timestamp": 1785943374.3520021
      }
    ],
    "stage2_medium": [
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 43830949
        },
        "timestamp": 1785941826.956319
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 220332373
        },
        "timestamp": 1785941828.28338
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 220332373
        },
        "timestamp": 1785941829.682229
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213774677
        },
        "timestamp": 1785941830.974171
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213774677
        },
        "timestamp": 1785941832.179095
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 78030091,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213774677
        },
        "timestamp": 1785941833.4533298
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 176230116,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213774677
        },
        "timestamp": 1785941834.6702
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 292512645,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213774677
        },
        "timestamp": 1785941835.879176
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 433173437,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213774677
        },
        "timestamp": 1785941837.098295
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 585025081,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213774677
        },
        "timestamp": 1785941838.347425
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 580786218,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 32402462,
          "works": 213774677
        },
        "timestamp": 1785941839.6775591
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 580786218,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 99417530,
          "works": 213774677
        },
        "timestamp": 1785941841.1442811
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 516250207,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 164439839,
          "works": 213774677
        },
        "timestamp": 1785941842.521177
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 516250207,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159073197,
          "work_institution": 9096130,
          "works": 213774677
        },
        "timestamp": 1785941843.8214889
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159073197,
          "work_institution": 45415690,
          "works": 213774677
        },
        "timestamp": 1785941845.0783901
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159073197,
          "work_institution": 69611092,
          "works": 213774677
        },
        "timestamp": 1785941846.3512478
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159073197,
          "work_institution": 104065513,
          "works": 213774677
        },
        "timestamp": 1785941847.606879
      },
      {
        "filesystem_bytes": 18049654784,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159073197,
          "work_institution": 100948553,
          "work_topic": 123405624,
          "works": 213774677
        },
        "timestamp": 1785941848.893169
      },
      {
        "filesystem_bytes": 21008642048,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159073197,
          "work_institution": 100948553,
          "work_topic": 202363701,
          "works": 213774677
        },
        "timestamp": 1785941850.304811
      }
    ],
    "stage2_small": [
      {
        "filesystem_bytes": 24876318720,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 43789930
        },
        "timestamp": 1785941490.375096
      },
      {
        "filesystem_bytes": 24876318720,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 110785365,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 43789930
        },
        "timestamp": 1785941491.608501
      },
      {
        "filesystem_bytes": 24876318720,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 107586178,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 40607995,
          "works": 43789930
        },
        "timestamp": 1785941492.837877
      },
      {
        "filesystem_bytes": 25202487296,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3342778720,
          "citation_edge": 107586178,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 40607995,
          "work_institution": 23579325,
          "work_topic": 38968252,
          "works": 43789930
        },
        "timestamp": 1785941494.014882
      }
    ]
  }
}
```

Scaling slopes are empirical evidence from sampled tiers; they are not a full-size prediction.

## Limitations

- This local Stage 2 run executed the requested 50 GiB ClickHouse container with 16 CPUs, 1 concurrent worker(s), and 8 query threads; no resource fallback was attempted.
- The OpenAlex manifests publish byte lengths and record counts but no content checksum; verification checks size and Parquet footer row counts and does not claim cryptographic object integrity.
- The Works samples are stratified by updated_date and are not a population-representative sample.
- Local Apple Silicon and local SSD latency is not extrapolated to an Alliance x86 VM with network-backed storage.
- The Alliance performance envelope remains unvalidated.
- stage2_small: the canonical Authors snapshot leaves 8133 of 3852081 Work-author bridge rows unresolved, including 8118 documented NULL-author rows and 0 documented deleted-author rows. The ordinary unresolved count is 15 of 3843963 (coverage 0.9999960978; blocking floor 0.999000). Raw links are preserved; use LEFT JOIN when unmatched authorships matter.
- stage2_medium: the canonical Authors snapshot leaves 33354 of 16075482 Work-author bridge rows unresolved, including 33089 documented NULL-author rows and 0 documented deleted-author rows. The ordinary unresolved count is 265 of 16042393 (coverage 0.9999834813; blocking floor 0.999000). Raw links are preserved; use LEFT JOIN when unmatched authorships matter.
- stage2_large: the canonical Authors snapshot leaves 98331 of 51816498 Work-author bridge rows unresolved, including 93593 documented NULL-author rows and 0 documented deleted-author rows. The ordinary unresolved count is 4738 of 51722905 (coverage 0.9999083965; blocking floor 0.999000). Raw links are preserved; use LEFT JOIN when unmatched authorships matter.
