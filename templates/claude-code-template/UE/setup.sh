#!/bin/bash
# Claude Code Template Setup Script (Bash)
# Interactive setup for configuring .claude directory in your project

set -e

TEMPLATE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "========================================"
echo "  Claude Code Template Setup"
echo "========================================"
echo ""

# --- Step 1: Target Directory ---
if [ -z "$1" ]; then
    read -p "Target project directory (full path): " TARGET_DIR
else
    TARGET_DIR="$1"
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "ERROR: Directory does not exist: $TARGET_DIR"
    exit 1
fi

echo ""
echo "Target: $TARGET_DIR"
echo ""

# --- Step 2: Project Info ---
read -p "Project name: " PROJECT_NAME
read -p "Project description (1 line): " PROJECT_DESC

echo ""
echo "Communication language options:"
echo "  1. Japanese (default)"
echo "  2. English"
read -p "Select [1/2]: " LANG_CHOICE
if [ "$LANG_CHOICE" = "2" ]; then
    USER_LANG="English"
    COMMENT_LANG="English"
else
    USER_LANG="Japanese"
    COMMENT_LANG="Japanese"
fi

read -p "Programming language (e.g., Python, C++, TypeScript): " PROG_LANG
read -p "Framework (e.g., PySide6, React, UE5) [optional]: " FRAMEWORK
read -p "Build/verify command (e.g., 'npm run build', 'python main.py'): " BUILD_CMD

echo ""
echo "Quick start commands (one per line, empty line to finish):"
QUICK_START=""
while true; do
    read -p "  > " line
    if [ -z "$line" ]; then break; fi
    if [ -n "$QUICK_START" ]; then
        QUICK_START="$QUICK_START\n$line"
    else
        QUICK_START="$line"
    fi
done

# --- Step 3: Copy base template ---
echo ""
echo "Copying base template..."

TARGET_CLAUDE="$TARGET_DIR/.claude"

if [ -d "$TARGET_CLAUDE" ]; then
    read -p ".claude directory already exists. Overwrite? [y/N]: " OVERWRITE
    if [ "$OVERWRITE" != "y" ] && [ "$OVERWRITE" != "Y" ]; then
        echo "Aborted."
        exit 0
    fi
fi

# Copy .claude directory
cp -r "$TEMPLATE_DIR/.claude" "$TARGET_DIR/"

# Process CLAUDE.md template
sed -e "s|{{PROJECT_NAME}}|$PROJECT_NAME|g" \
    -e "s|{{PROJECT_DESCRIPTION}}|$PROJECT_DESC|g" \
    -e "s|{{USER_LANGUAGE}}|$USER_LANG|g" \
    -e "s|{{COMMENT_LANGUAGE}}|$COMMENT_LANG|g" \
    -e "s|{{BUILD_COMMAND}}|$BUILD_CMD|g" \
    -e "s|{{QUICK_START_COMMANDS}}|$(echo -e "$QUICK_START")|g" \
    "$TEMPLATE_DIR/CLAUDE.md.template" > "$TARGET_DIR/CLAUDE.md"

# Process project overview
sed -e "s|{{PROJECT_DESCRIPTION}}|$PROJECT_DESC|g" \
    -e "s|{{LANGUAGE}}|$PROG_LANG|g" \
    -e "s|{{FRAMEWORK}}|$FRAMEWORK|g" \
    -e "s|{{QUICK_START_COMMANDS}}|$(echo -e "$QUICK_START")|g" \
    -e "s|{{BUILD_COMMAND}}|$BUILD_CMD|g" \
    -e "s|{{FEATURE_1}}|(TODO: Add feature 1)|g" \
    -e "s|{{FEATURE_2}}|(TODO: Add feature 2)|g" \
    -e "s|{{FEATURE_3}}|(TODO: Add feature 3)|g" \
    "$TARGET_CLAUDE/rules/01-project-overview.md.template" > "$TARGET_CLAUDE/rules/01-project-overview.md"
rm -f "$TARGET_CLAUDE/rules/01-project-overview.md.template"

# Process project structure
sed -e "s|{{PROJECT_NAME}}|$PROJECT_NAME|g" \
    -e "s|{{SOURCE_DIR}}|src|g" \
    -e "s|{{CONFIG_DIR}}|config|g" \
    -e "s|{{TEST_DIR}}|tests|g" \
    -e "s|{{DOC_DIR}}|docs|g" \
    "$TARGET_CLAUDE/rules/02-project-structure.md.template" > "$TARGET_CLAUDE/rules/02-project-structure.md"
rm -f "$TARGET_CLAUDE/rules/02-project-structure.md.template"

# Update settings.json language
if [ "$USER_LANG" = "English" ]; then
    sed -i 's/"language": "japanese"/"language": "english"/' "$TARGET_CLAUDE/settings.json"
fi

echo "Base template installed."

# --- Step 4: Addons ---
echo ""
echo "========================================"
echo "  Available Addons"
echo "========================================"

ADDONS_DIR="$TEMPLATE_DIR"

if [ -d "$ADDONS_DIR" ]; then
    for addon_dir in "$ADDONS_DIR"/*/; do
        addon_name=$(basename "$addon_dir")
        [ "$addon_name" = ".claude" ] && continue
        echo ""
        echo "  [$addon_name]"
        for sub_dir in "$addon_dir"*/; do
            if [ -d "$sub_dir" ]; then
                sub_name=$(basename "$sub_dir")
                files=$(find "$sub_dir" -type f -name "*.md" -o -name "*.json" -o -name "*.template" | xargs -I{} basename {} | tr '\n' ', ' | sed 's/,$//')
                echo "    $sub_name/: $files"
            fi
        done
    done

    echo ""
    read -p "Install addons? (comma-separated, e.g., 'ue' or 'all' or 'none'): " INSTALL_ADDONS

    if [ "$INSTALL_ADDONS" != "none" ] && [ -n "$INSTALL_ADDONS" ]; then
        if [ "$INSTALL_ADDONS" = "all" ]; then
            SELECTED=$(ls -d "$ADDONS_DIR"/*/ 2>/dev/null | xargs -I{} basename {})
        else
            SELECTED=$(echo "$INSTALL_ADDONS" | tr ',' ' ')
        fi

        for addon_name in $SELECTED; do
            addon_path="$ADDONS_DIR/$addon_name"
            if [ ! -d "$addon_path" ]; then
                echo "  Addon '$addon_name' not found, skipping."
                continue
            fi

            echo "  Installing addon: $addon_name..."

            # UE addon specific
            if [ "$addon_name" = "ue" ]; then
                read -p "    UE version (e.g., 5.5): " UE_VERSION
                read -p "    UE engine path: " UE_ENGINE_PATH
                read -p "    UE project path: " UE_PROJECT_PATH
            fi

            # Copy addon files
            for sub_dir in "$addon_path"/*/; do
                if [ ! -d "$sub_dir" ]; then continue; fi
                sub_name=$(basename "$sub_dir")
                target_sub="$TARGET_CLAUDE/$sub_name"
                mkdir -p "$target_sub"

                find "$sub_dir" -type f | while read -r file; do
                    rel_path="${file#$sub_dir}"
                    dest_path="$target_sub/$rel_path"
                    dest_dir=$(dirname "$dest_path")
                    mkdir -p "$dest_dir"

                    if [ "$addon_name" = "ue" ]; then
                        sed -e "s|{{UE_VERSION}}|UE $UE_VERSION|g" \
                            -e "s|{{UE_ENGINE_PATH}}|$UE_ENGINE_PATH|g" \
                            -e "s|{{PROJECT_NAME}}|$PROJECT_NAME|g" \
                            -e "s|{{PROJECT_PATH}}|$UE_PROJECT_PATH|g" \
                            "$file" > "$dest_path"
                    else
                        cp "$file" "$dest_path"
                    fi

                    # Remove .template extension
                    if [[ "$dest_path" == *.template ]]; then
                        mv "$dest_path" "${dest_path%.template}"
                    fi
                done
            done

            echo "  Addon '$addon_name' installed."
        done
    fi
fi

# --- Step 5: Summary ---
echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "Installed to: $TARGET_DIR"
echo ""
echo "Files created:"
find "$TARGET_CLAUDE" -type f | while read -r f; do
    echo "  ${f#$TARGET_DIR/}"
done
if [ -f "$TARGET_DIR/CLAUDE.md" ]; then
    echo "  CLAUDE.md"
fi

echo ""
echo "Next steps:"
echo "  1. Review and customize CLAUDE.md"
echo "  2. Edit .claude/rules/01-project-overview.md"
echo "  3. Edit .claude/rules/02-project-structure.md"
echo "  4. Configure build commands in skills/dev/ and skills/verify/"
echo "  5. Start Claude Code in your project: cd $TARGET_DIR && claude"
echo ""
