# Contributing to MCPStore Plugins

Thank you for contributing! This repository holds community-maintained client plugins for [MCPStore](https://github.com/ip2a/mcpstore).

## Quick Start

1. Fork this repository
2. Copy an existing plugin folder (e.g., `claude/`) as a template
3. Edit `plugin.toml` with your client's configuration
4. Test locally: `mcpstore plugin validate your-client/`
5. Submit a Pull Request

## Plugin Structure

Each plugin is a folder under `clients/` containing at least `plugin.toml`:

```
clients/
  your-client/
    plugin.toml    # Required manifest
    icon.svg       # Optional icon
```

## Manifest Requirements

Your `plugin.toml` must:

1. **Match the schema**: See `plugin.schema.json` and `README.md` for field definitions
2. **Use a unique ID**: Check existing plugins to avoid collisions
3. **Follow naming conventions**: `plugin.id` must match `^[a-z][a-z0-9-]*$`
4. **Set correct paths**: Use `~` for home directory or absolute paths only
5. **List exact supported fields**: Any unlisted field will cause import rejection

## Testing Your Plugin

Before submitting:

```bash
# Validate manifest syntax and schema
mcpstore plugin validate clients/your-client/

# Test discovery (requires the client installed)
mcpstore clients list

# Test import (requires a real config file)
mcpstore import your-client
```

## Submission Criteria

Your PR will be automatically merged if:

1. ✅ CI passes (schema validation + TOML syntax)
2. ✅ No duplicate `plugin.id`
3. ✅ Folder name matches `plugin.id`
4. ✅ All required fields present

Manual review is only needed for:

- Changes to `README.md` or `CONTRIBUTING.md`
- New field types not covered by schema
- Plugins requiring special installation instructions

## Plugin Guidelines

### Discovery Paths

- **Research first**: Check the client's documentation for official config paths
- **Test on target OS**: Verify paths on macOS/Linux/Windows if claiming cross-platform
- **Use platform overrides**: Add `config_paths_macos`, `_linux`, `_windows` when paths differ

### Supported Fields

- **Be conservative**: Only list fields you've tested or seen in documentation
- **Don't guess**: Unknown fields cause import failures for users
- **Document sources**: Add a comment in your PR linking to the client's config schema

### Gateway Entry

- **Test remote servers**: If claiming `supports_remote = true`, verify the client actually accepts HTTP URLs
- **Match client format**: Set `extra` fields to match what the client expects (e.g., OpenCode's `type` field)

## Examples

See built-in plugins for reference:

- **Standard JSON format**: `claude/`, `cursor/`
- **TOML format**: `codex/`
- **Array command syntax**: `opencode/`
- **Extended fields**: `pi/`, `omp/`
- **Type validation**: `opencode/` (see `validate_type_field`)

## Questions?

- Read the [Plugin Specification](README.md)
- Check existing plugin manifests for patterns
- Open an issue if something is unclear

## License

By contributing, you agree your contributions will be licensed under the same license as MCPStore (check main repository).
