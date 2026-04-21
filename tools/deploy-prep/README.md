# deploy-prep

Deploy preparation tools for ExpertPack. These tools produce clean, deploy-ready copies of a pack without modifying the source.

## ep-strip-frontmatter.py

Strips YAML frontmatter (`---...---` blocks) from all `.md` files in a pack before indexing.

**Why:** Provenance frontmatter (`id`, `content_hash`, `verified_at`, `verified_by`) is management metadata — it serves tooling and freshness tracking, not retrieval. Embedding it alongside content dilutes semantic similarity scores and wastes context tokens.

**Principle:** Source files (in the ExpertPacks repo) retain full provenance. The help bot indexes clean files. Deploy artifacts are ephemeral and gitignored.

### Usage

```bash
# Standard deploy prep
python3 ep-strip-frontmatter.py --src ./my-pack --out ./my-pack-deploy

# Dry run — see what would be stripped
python3 ep-strip-frontmatter.py --src ./my-pack --out ./my-pack-deploy --dry-run

# Suppress overwrite warning
python3 ep-strip-frontmatter.py --src ./my-pack --out ./my-pack-deploy --force
```

### Recommended deploy pattern

```bash
# 1. Strip frontmatter to a temp deploy dir
python3 expert-pack/tools/deploy-prep/ep-strip-frontmatter.py \
    --src ExpertPacks/my-pack \
    --out /tmp/my-pack-deploy \
    --force

# 2. Package and ship
tar czf /tmp/my-pack-deploy.tar.gz -C /tmp/my-pack-deploy .
scp /tmp/my-pack-deploy.tar.gz user@your-server:/tmp/
ssh user@your-server "rm -rf /path/to/my-pack && \
    mkdir -p /path/to/my-pack && \
    tar xzf /tmp/my-pack-deploy.tar.gz -C /path/to/my-pack"

# 3. Clean up
rm -rf /tmp/my-pack-deploy /tmp/my-pack-deploy.tar.gz
```
