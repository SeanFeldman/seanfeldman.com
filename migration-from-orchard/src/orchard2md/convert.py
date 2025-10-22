from __future__ import annotations

import re
from markdownify import markdownify as md


def convert_html_to_markdown(html: str) -> str:
    """Convert HTML to Markdown with sensible defaults.

    - Preserve links and images
    - Convert strong/emphasis
    - Keep simple tables
    - Convert code blocks marked with csharpcode/codeSnippet divs
    - Detect and preserve content that's already in Markdown format
    """
    if not html:
        return ""
    
    # Check if content is already Markdown (contains reference-style links or has minimal HTML)
    if _is_likely_markdown(html):
        # Content is already Markdown, just clean up indented code blocks
        return _preprocess_code_blocks(html)
    
    # Pre-process: convert <div class="csharpcode"> or <div id="codeSnippet"> blocks to proper code blocks
    html = _preprocess_code_blocks(html)
    
    return md(html, heading_style="ATX")


def _is_likely_markdown(text: str) -> bool:
    """Detect if content is already in Markdown format rather than HTML."""
    # Check for reference-style link definitions at the end: [1]: http://...
    if re.search(r'\[\d+\]:\s+https?://', text):
        return True
    
    # Check for Markdown headings (## or ###)
    if re.search(r'^#{2,}\s+\w+', text, re.MULTILINE):
        return True
    
    # If it has very few HTML tags (excluding code blocks), it's likely Markdown
    # Count HTML tags excluding <pre>, <code>, and entities
    html_tag_count = len(re.findall(r'<(?!/?(?:pre|code)\b)[a-z][^>]*>', text, re.IGNORECASE))
    
    # If less than 3 HTML tags, probably Markdown
    return html_tag_count < 3


def _format_csharp_code(code: str) -> str:
    """Apply C# formatting rules to remove ALL blank lines from code blocks."""
    lines = code.split('\n')
    # Simply keep only non-empty lines
    result = [line for line in lines if line.strip()]
    return '\n'.join(result)


def _preprocess_code_blocks(html: str) -> str:
    """Convert blog-specific code block divs and indented code into proper <pre><code> blocks."""
    
    # Detect if this is Markdown content
    is_markdown = _is_likely_markdown(html)
    
    # Pattern 1: <div class="csharpcode">...<pre>...code...</pre>...</div>
    # Pattern 2: <div id="codeSnippet">...<pre>...code...</pre>...</div>
    # These often contain &#xA; (newlines) and &#x9; (tabs) entities
    
    def extract_code_from_pre_tags(match):
        """Extract code from <pre> tags within the matched div."""
        div_content = match.group(1)
        
        # Find all <pre> tags and extract their text content
        pre_pattern = r'<pre[^>]*>(.*?)</pre>'
        pre_matches = re.findall(pre_pattern, div_content, re.DOTALL | re.IGNORECASE)
        
        if not pre_matches:
            # No pre tags found, return original
            return match.group(0)
        
        # Combine all pre tag contents
        code_lines = []
        for pre_content in pre_matches:
            # Strip HTML tags (like <span class="lnum">, <span class="kwrd">, etc.)
            clean_line = re.sub(r'<[^>]+>', '', pre_content)
            # Decode HTML entities
            clean_line = clean_line.replace('&#xA;', '\n')
            clean_line = clean_line.replace('&#x9;', '\t')
            clean_line = clean_line.replace('&lt;', '<')
            clean_line = clean_line.replace('&gt;', '>')
            clean_line = clean_line.replace('&quot;', '"')
            clean_line = clean_line.replace('&amp;', '&')
            clean_line = clean_line.replace('&nbsp;', ' ')
            if clean_line.strip():
                code_lines.append(clean_line.rstrip())
        
        # Return as a proper code block (will be converted to Markdown later)
        code = '\n'.join(code_lines)
        return f'<pre><code class="language-csharp">\n{code}\n</code></pre>'
    
    # Match div blocks with class="csharpcode" or id="codeSnippet" or id="codeSnippetWrapper"
    pattern = r'<div\s+(?:class="csharpcode"|id="codeSnippet(?:Wrapper)?")[^>]*>(.*?)</div>(?:\s*<style[^>]*>.*?</style>)?'
    html = re.sub(pattern, extract_code_from_pre_tags, html, flags=re.DOTALL | re.IGNORECASE)
    
    # Pattern 3: Detect Markdown-style 4-space indented code blocks
    # These appear as: blank line, then lines starting with 4 spaces
    # First decode entities to work with actual whitespace
    def detect_and_wrap_indented_code(text, as_markdown=False):
        """Detect 4-space indented code blocks and wrap them in pre/code tags or fenced code blocks."""
        # Decode entities first
        decoded = text.replace('&#xD;&#xA;', '\n')
        decoded = decoded.replace('&#xA;', '\n')
        decoded = decoded.replace('&#x9;', '\t')
        
        lines = decoded.split('\n')
        result = []
        in_code_block = False
        code_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Skip reference-style link definitions (they shouldn't be treated as code)
            # Pattern: [number]: url or [text]: url
            if re.match(r'^\s*\[.+?\]:\s+https?://', line):
                if in_code_block:
                    # End any active code block before this link definition
                    code = '\n'.join(code_lines).strip()
                    if code:
                        if as_markdown:
                            result.append(f'```\n{code}\n```')
                        else:
                            code = code.replace('&', '&amp;')
                            code = code.replace('<', '&lt;')
                            code = code.replace('>', '&gt;')
                            code = code.replace('"', '&quot;')
                            result.append(f'<pre><code class="language-csharp">{code}</code></pre>')
                    in_code_block = False
                    code_lines = []
                # Add the link definition without indentation
                result.append(line.lstrip())
                i += 1
                continue
            
            # Check if this is an indented code line (4+ spaces) or blank line within code
            if line.startswith('    '):
                if not in_code_block:
                    in_code_block = True
                    code_lines = []
                # Add line with indentation removed
                stripped = line[4:] if len(line) > 4 else ''
                # Only add if the line has actual content (not just whitespace)
                # This prevents lines like "    " from becoming empty lines in code
                if stripped.strip():
                    code_lines.append(stripped.rstrip())  # Also remove trailing whitespace
            elif not line.strip() and in_code_block:
                # Completely blank line within code block - skip it (don't preserve extra spacing)
                pass
            else:
                # Non-indented, non-blank line - end of code block
                if in_code_block:
                    # Apply C# formatting rules
                    code = _format_csharp_code('\n'.join(code_lines).strip())
                    
                    if as_markdown:
                        # For Markdown content, use fenced code blocks with C# syntax highlighting
                        result.append(f'```csharp\n{code}\n```')
                    else:
                        # For HTML content, encode and wrap in pre/code
                        code = code.replace('&', '&amp;')
                        code = code.replace('<', '&lt;')
                        code = code.replace('>', '&gt;')
                        code = code.replace('"', '&quot;')
                        result.append(f'<pre><code class="language-csharp">{code}</code></pre>')
                    
                    in_code_block = False
                    code_lines = []
                
                # Add the non-code line
                if line or i < len(lines) - 1:  # Keep blank lines except trailing
                    result.append(line)
            
            i += 1
        
        # Handle case where code block is at the end
        if in_code_block:
            # Apply C# formatting rules
            code = _format_csharp_code('\n'.join(code_lines).strip())
            
            if as_markdown:
                result.append(f'```csharp\n{code}\n```')
            else:
                code = code.replace('&', '&amp;')
                code = code.replace('<', '&lt;')
                code = code.replace('>', '&gt;')
                code = code.replace('"', '&quot;')
                result.append(f'<pre><code class="language-csharp">{code}</code></pre>')
        
        return '\n'.join(result)
    
    html = detect_and_wrap_indented_code(html, as_markdown=is_markdown)
    
    return html
