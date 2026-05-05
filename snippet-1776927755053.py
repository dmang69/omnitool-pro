return resolved_path == current_dir or current_dir in resolved_path.parents
# should be:
return str(resolved_path).startswith(str(current_dir))