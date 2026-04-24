/**
 * Music Player Module - Manages audio playback and playlist functionality
 * Handles play/pause, next/previous, progress tracking
 */

class MusicPlayer {
  constructor(config = {}) {
    this.audio = config.audio;
    this.playBtn = config.playBtn;
    this.prevBtn = config.prevBtn;
    this.nextBtn = config.nextBtn;
    this.progress = config.progress;
    this.progressContainer = config.progressContainer;
    this.cover = config.cover;
    this.musicTitle = config.musicTitle;

    this.isPlaying = false;
    this.currentSongIndex = 0;
    this.songs = config.songs || [];

    this.init();
  }

  init() {
    this.attachEventListeners();
    if (this.songs.length > 0) {
      this.loadSong(0);
    }
  }

  attachEventListeners() {
    this.playBtn.addEventListener('click', () => this.togglePlay());
    this.prevBtn.addEventListener('click', () => this.prevSong());
    this.nextBtn.addEventListener('click', () => this.nextSong());
    this.audio.addEventListener('timeupdate', () => this.updateProgress());
    this.progressContainer.addEventListener('click', (e) => this.setProgress(e));
    this.audio.addEventListener('ended', () => this.nextSong());
  }

  loadSong(index) {
    if (index < 0 || index >= this.songs.length) return;
    
    const song = this.songs[index];
    this.audio.src = song.src;
    this.cover.src = song.cover;
    this.musicTitle.textContent = song.title;
    this.currentSongIndex = index;
  }

  play() {
    this.isPlaying = true;
    this.playBtn.classList.add('playing');
    const icon = this.playBtn.querySelector('i');
    icon.classList.remove('fa-play');
    icon.classList.add('fa-pause');
    this.audio.play().catch(e => console.log('Audio play failed:', e));
  }

  pause() {
    this.isPlaying = false;
    this.playBtn.classList.remove('playing');
    const icon = this.playBtn.querySelector('i');
    icon.classList.add('fa-play');
    icon.classList.remove('fa-pause');
    this.audio.pause();
  }

  togglePlay() {
    if (this.isPlaying) {
      this.pause();
    } else {
      this.play();
    }
  }

  nextSong() {
    this.currentSongIndex = (this.currentSongIndex + 1) % this.songs.length;
    this.loadSong(this.currentSongIndex);
    if (this.isPlaying) {
      this.play();
    }
  }

  prevSong() {
    this.currentSongIndex = (this.currentSongIndex - 1 + this.songs.length) % this.songs.length;
    this.loadSong(this.currentSongIndex);
    if (this.isPlaying) {
      this.play();
    }
  }

  updateProgress() {
    if (this.audio.duration) {
      const progressPercent = (this.audio.currentTime / this.audio.duration) * 100;
      this.progress.style.width = `${progressPercent}%`;
    }
  }

  setProgress(e) {
    const width = this.progressContainer.clientWidth;
    const clickX = e.offsetX;
    const duration = this.audio.duration;
    this.audio.currentTime = (clickX / width) * duration;
  }
}

export default MusicPlayer;
