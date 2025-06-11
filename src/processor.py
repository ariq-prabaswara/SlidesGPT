import os
import pypandoc
from .utils import logger

class SlideProcessor:
    def __init__(self):
        """Initialize the slide processor"""
        self.ensure_pandoc()

    def ensure_pandoc(self):
        """Ensure pandoc is available, download if needed"""
        try:
            pypandoc.get_pandoc_version()
        except OSError:
            logger.info("Pandoc not found. Downloading pandoc...")
            try:
                pypandoc.download_pandoc()
                logger.info("Successfully downloaded pandoc")
            except Exception as e:
                logger.error(f"Failed to download pandoc: {str(e)}")
                raise RuntimeError("Failed to download pandoc. Please install it manually from https://pandoc.org/installing.html")

    def validate_markdown(self, content: str) -> bool:
        """Validate the markdown structure"""
        required_elements = [
            ('# ', 'Title slide'),
            ('## ', 'Slide titles'),
            ('---', 'Slide separators'),
            ('- ', 'Bullet points')
        ]
        
        for element, name in required_elements:
            if element not in content:
                logger.error(f"Missing {name} in the markdown content")
                return False
        return True

    def post_process_markdown(self, content: str) -> str:
        """Clean up and format the markdown content"""
        # Remove extra blank lines
        lines = content.split('\n')
        cleaned_lines = []
        prev_empty = False
        
        for line in lines:
            is_empty = not line.strip()
            if not (is_empty and prev_empty):
                cleaned_lines.append(line)
            prev_empty = is_empty
        
        return '\n'.join(cleaned_lines)

    def convert_to_pptx(self, markdown_file: str, output_file: str) -> bool:
        """Convert markdown file to PowerPoint using pypandoc"""
        try:
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
            
            # Convert markdown to PowerPoint
            extra_args = ['--slide-level=2']  # Use ## as slide breaks
            if os.path.exists('template.pptx'):
                extra_args.append('--reference-doc=template.pptx')
            
            pypandoc.convert_file(
                markdown_file,
                'pptx',
                outputfile=output_file,
                extra_args=extra_args
            )
            
            logger.info(f"Successfully converted {markdown_file} to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error converting to PowerPoint: {str(e)}")
            return False

    def process(self, content: str, output_file: str) -> bool:
        """Process the content and convert to PowerPoint"""
        try:
            # Validate markdown structure
            if not self.validate_markdown(content):
                return False
            
            # Post-process the markdown
            processed_content = self.post_process_markdown(content)
            
            # Save markdown file
            markdown_file = output_file.replace('.pptx', '.md')
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(processed_content)
            
            # Convert to PowerPoint
            return self.convert_to_pptx(markdown_file, output_file)
            
        except Exception as e:
            logger.error(f"Error processing content: {str(e)}")
            return False 