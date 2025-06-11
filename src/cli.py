import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from .gemini import GeminiService
from .processor import SlideProcessor
from .utils import logger, ensure_output_dir
import os

console = Console()

@click.group()
def cli():
    """SlidesGPT - Convert plain text to presentation slides"""
    pass

@cli.command()
@click.option('--input', '-i', help='Input file path')
@click.option('--text', '-t', help='Direct text input')
@click.option('--output', '-o', required=True, help='Output file path (will be saved as .pptx)')
def generate(input, text, output):
    """Generate presentation slides from text input"""
    if not input and not text:
        console.print(Panel.fit(
            "[red]Error: Either --input or --text must be provided[/red]",
            title="Error"
        ))
        return

    try:
        # Ensure output has .pptx extension
        if not output.endswith('.pptx'):
            output = output.rsplit('.', 1)[0] + '.pptx'
            
        # Ensure output directory exists
        ensure_output_dir(output)
        
        # Get input content
        content = ""
        if input:
            with open(input, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = text

        # Initialize services
        gemini = GeminiService()
        processor = SlideProcessor()
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Processing...", total=100)
            
            # Process content with Gemini
            result = gemini.process_content(content)
            
            # Process and convert to PowerPoint
            if result and processor.process(result, output):
                progress.update(task, completed=100)
                console.print(Panel.fit(
                    f"[green]Successfully generated presentation at: {output}[/green]",
                    title="Success"
                ))
            else:
                console.print(Panel.fit(
                    "[red]Error: Failed to generate valid presentation content[/red]",
                    title="Error"
                ))
                
    except Exception as e:
        logger.error(f"Error during generation: {str(e)}")
        console.print(Panel.fit(
            f"[red]Error: {str(e)}[/red]",
            title="Error"
        ))

if __name__ == '__main__':
    cli() 