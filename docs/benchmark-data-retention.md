# Benchmark data retention

For future benchmarks, preserve the largest verified raw/normalized corpus and reusable snapshots of prepared databases. Retire the older, smaller retained copy only after validating its replacement; record the volume/snapshot IDs, engine versions, schema, exact cohort manifest and verification results alongside the study.

A 200m corpus can supply the exact 100m subset without another download. A clean 100m scaling benchmark still needs a database physically built from that subset, since filtering a 200m database measures a different workload. Database snapshots should be consistent and recoverable before the original prepared volumes are deleted.

This policy applies to future work. In the completed 12 November 2026 study, the new 200m volumes were deleted without snapshots, and only the older raw-data EBS volume was retained. The historical experiment scripts document that run; their cleanup settings do not supersede this retention policy.
