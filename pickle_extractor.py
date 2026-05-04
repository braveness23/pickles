#!/usr/bin/env python3
"""
Pickle Extractor 3000
Downloads YouTube video, isolates vocals, extracts all instances of a target word
"""

import whisper
import subprocess
import sys
from pydub import AudioSegment
from pathlib import Path
import shutil

def check_dependencies():
    """Check if required tools are installed"""
    dependencies = {
        'yt-dlp': 'pip install yt-dlp',
        'ffmpeg': 'apt install ffmpeg  # or brew install ffmpeg',
        'demucs': 'pip install demucs'
    }
    
    missing = []
    for cmd, install in dependencies.items():
        if not shutil.which(cmd):
            missing.append(f"  {cmd}: {install}")
    
    if missing:
        print("Missing dependencies:")
        print("\n".join(missing))
        sys.exit(1)

def download_youtube_audio(url, output_file="youtube_audio.wav"):
    """Download audio from YouTube video"""
    print(f"📥 Downloading audio from YouTube...")
    
    cmd = [
        'yt-dlp',
        '-x',  # Extract audio
        '--audio-format', 'wav',
        '--output', output_file,
        url
    ]
    
    subprocess.run(cmd, check=True)
    print(f"✓ Downloaded: {output_file}")
    return output_file

def isolate_vocals(audio_file, output_dir="separated"):
    """Use Demucs to isolate vocals from background music"""
    print(f"🎤 Isolating vocals with Demucs...")
    
    cmd = [
        'demucs',
        '--two-stems=vocals',
        '--mp3',
        '--mp3-bitrate=320',
        '-o', output_dir,
        audio_file
    ]
    
    subprocess.run(cmd, check=True)
    
    # Demucs creates: separated/htdemucs/youtube_audio/vocals.mp3
    vocals_path = Path(output_dir) / 'htdemucs' / Path(audio_file).stem / 'vocals.mp3'
    print(f"✓ Vocals isolated: {vocals_path}")
    return vocals_path

def extract_word_samples(vocals_file, target_word="pickles", model_size="medium", padding_ms=100, pre_buffer_ms=1000):
    """Extract all instances of target word using Whisper"""
    print(f"🔍 Finding all instances of '{target_word}'...")
    
    # Load Whisper model
    print(f"Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size)
    
    # Transcribe with word timestamps
    print("Transcribing audio...")
    result = model.transcribe(str(vocals_file), word_timestamps=True)
    
    # Load audio
    print("Loading audio for extraction...")
    audio = AudioSegment.from_file(vocals_file)
    
    # Create output directory
    word_slug = target_word.lower()
    output_dir = Path(f"{word_slug}_samples")
    output_dir.mkdir(exist_ok=True)

    # Extract each instance
    sample_count = 0

    for segment in result['segments']:
        for word_info in segment.get('words', []):
            word = word_info['word'].strip().lower()
            word_clean = ''.join(c for c in word if c.isalnum())

            if target_word.lower() in word_clean:
                start_time = word_info['start'] * 1000  # ms
                end_time = word_info['end'] * 1000

                # Add padding and pre-buffer
                start_with_padding = max(0, start_time - pre_buffer_ms)
                end_with_padding = min(len(audio), end_time + padding_ms)

                # Extract and normalize
                sample = audio[start_with_padding:end_with_padding]
                sample = sample.normalize()

                # Export
                sample_count += 1
                timestamp = f"{int(start_time/1000):03d}s"
                output_file = output_dir / f"{word_slug}_{sample_count:03d}_{timestamp}.wav"

                sample.export(output_file, format="wav")
                print(f"  ✓ {output_file} ({end_time - start_time:.0f}ms)")

    # Save transcript
    transcript_file = output_dir / "transcript.txt"
    with open(transcript_file, 'w') as f:
        f.write(result['text'])

    print(f"\n🎉 Extracted {sample_count} '{target_word}' samples!")
    print(f"📁 Output: {output_dir}/")
    print(f"📄 Transcript: {transcript_file}")
    
    return sample_count

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Extract word samples from YouTube video",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pickle_extractor.py "https://youtube.com/watch?v=..."
  python pickle_extractor.py "https://youtube.com/watch?v=..." --word cucumber
  python pickle_extractor.py "https://youtube.com/watch?v=..." --word biden
  python pickle_extractor.py "https://youtube.com/watch?v=..." --word trump --model small --padding 150
        """
    )
    
    parser.add_argument("url", help="YouTube URL")
    parser.add_argument("-w", "--word", default="pickles", help="Word to extract (default: pickles)")
    parser.add_argument("-m", "--model", default="medium",
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help="Whisper model size (default: medium)")
    parser.add_argument("-p", "--padding", type=int, default=100,
                       help="Padding in ms around each word (default: 100)")
    parser.add_argument("--keep-temp", action="store_true",
                       help="Keep temporary files (audio download, separated vocals)")
    parser.add_argument("--skip-vocal-isolation", action="store_true",
                       help="Skip vocal isolation and transcribe full audio (faster, less accurate)")
    
    args = parser.parse_args()
    
    # Check dependencies
    check_dependencies()
    
    try:
        # Download audio
        audio_file = download_youtube_audio(args.url)
        
        # Isolate vocals (or skip)
        if args.skip_vocal_isolation:
            print("⚡ Skipping vocal isolation, using full audio...")
            vocals_file = audio_file
        else:
            vocals_file = isolate_vocals(audio_file)
        
        # Extract samples
        sample_count = extract_word_samples(
            vocals_file,
            target_word=args.word,
            model_size=args.model,
            padding_ms=args.padding
        )
        
        # Cleanup
        if not args.keep_temp:
            print("\n🧹 Cleaning up temporary files...")
            Path(audio_file).unlink(missing_ok=True)
            shutil.rmtree("separated", ignore_errors=True)
        
        print(f"\n✨ Done! Load samples into Reason and make some {args.word} music!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Command failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()