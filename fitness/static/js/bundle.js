(() => {
  // src/js/timer.js
  var Timer = class {
    constructor(config = {}) {
      this.sessionInput = config.sessionInput;
      this.breakInput = config.breakInput;
      this.minutesDisplay = config.minutesDisplay;
      this.secondsDisplay = config.secondsDisplay;
      this.timerLabel = config.timerLabel;
      this.startBtn = config.startBtn;
      this.pauseBtn = config.pauseBtn;
      this.resetBtn = config.resetBtn;
      this.onSessionChange = config.onSessionChange || null;
      this.timer = null;
      this.isSession = true;
      this.timeLeft = parseInt(this.sessionInput.value) * 60;
      this.isRunning = false;
      this.init();
    }
    init() {
      this.updateDisplay();
      this.attachEventListeners();
    }
    attachEventListeners() {
      this.startBtn.addEventListener("click", () => this.start());
      this.pauseBtn.addEventListener("click", () => this.pause());
      this.resetBtn.addEventListener("click", () => this.reset());
      this.sessionInput.addEventListener("change", () => {
        if (!this.isRunning) {
          this.timeLeft = parseInt(this.sessionInput.value) * 60;
          this.updateDisplay();
        }
      });
      this.breakInput.addEventListener("change", () => {
        if (!this.isRunning && !this.isSession) {
          this.timeLeft = parseInt(this.breakInput.value) * 60;
          this.updateDisplay();
        }
      });
    }
    updateDisplay() {
      const min = String(Math.floor(this.timeLeft / 60)).padStart(2, "0");
      const sec = String(this.timeLeft % 60).padStart(2, "0");
      this.minutesDisplay.textContent = min;
      this.secondsDisplay.textContent = sec;
      this.timerLabel.textContent = this.isSession ? "Work Session" : "Break Time";
    }
    start() {
      if (this.timer)
        return;
      this.isRunning = true;
      this.startBtn.disabled = true;
      this.pauseBtn.disabled = false;
      this.startBtn.textContent = "Running...";
      this.timer = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--;
          this.updateDisplay();
        } else {
          this.switchSession();
        }
      }, 1e3);
    }
    switchSession() {
      this.isSession = !this.isSession;
      this.timeLeft = (this.isSession ? parseInt(this.sessionInput.value) : parseInt(this.breakInput.value)) * 60;
      this.updateDisplay();
      if (this.onSessionChange) {
        this.onSessionChange(this.isSession);
      }
    }
    pause() {
      clearInterval(this.timer);
      this.timer = null;
      this.isRunning = false;
      this.startBtn.disabled = false;
      this.pauseBtn.disabled = true;
      this.startBtn.textContent = "Resume";
    }
    reset() {
      clearInterval(this.timer);
      this.timer = null;
      this.isRunning = false;
      this.isSession = true;
      this.timeLeft = parseInt(this.sessionInput.value) * 60;
      this.updateDisplay();
      this.startBtn.disabled = false;
      this.pauseBtn.disabled = true;
      this.startBtn.textContent = "Start";
    }
  };
  var timer_default = Timer;

  // src/js/musicPlayer.js
  var MusicPlayer = class {
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
      this.playBtn.addEventListener("click", () => this.togglePlay());
      this.prevBtn.addEventListener("click", () => this.prevSong());
      this.nextBtn.addEventListener("click", () => this.nextSong());
      this.audio.addEventListener("timeupdate", () => this.updateProgress());
      this.progressContainer.addEventListener("click", (e) => this.setProgress(e));
      this.audio.addEventListener("ended", () => this.nextSong());
    }
    loadSong(index) {
      if (index < 0 || index >= this.songs.length)
        return;
      const song = this.songs[index];
      this.audio.src = song.src;
      this.cover.src = song.cover;
      this.musicTitle.textContent = song.title;
      this.currentSongIndex = index;
    }
    play() {
      this.isPlaying = true;
      this.playBtn.classList.add("playing");
      const icon = this.playBtn.querySelector("i");
      icon.classList.remove("fa-play");
      icon.classList.add("fa-pause");
      this.audio.play().catch((e) => console.log("Audio play failed:", e));
    }
    pause() {
      this.isPlaying = false;
      this.playBtn.classList.remove("playing");
      const icon = this.playBtn.querySelector("i");
      icon.classList.add("fa-play");
      icon.classList.remove("fa-pause");
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
        const progressPercent = this.audio.currentTime / this.audio.duration * 100;
        this.progress.style.width = `${progressPercent}%`;
      }
    }
    setProgress(e) {
      const width = this.progressContainer.clientWidth;
      const clickX = e.offsetX;
      const duration = this.audio.duration;
      this.audio.currentTime = clickX / width * duration;
    }
  };
  var musicPlayer_default = MusicPlayer;

  // src/js/main.js
  var timer = new timer_default({
    sessionInput: document.getElementById("session-length"),
    breakInput: document.getElementById("break-length"),
    minutesDisplay: document.getElementById("minutes"),
    secondsDisplay: document.getElementById("seconds"),
    timerLabel: document.getElementById("timer-label"),
    startBtn: document.getElementById("start"),
    pauseBtn: document.getElementById("pause"),
    resetBtn: document.getElementById("reset"),
    onSessionChange: (isSession) => {
      if (musicPlayer && musicPlayer.audio && musicPlayer.audio.readyState >= 2) {
        musicPlayer.audio.play().catch((e) => console.log("Audio play failed:", e));
      }
    }
  });
  var songs = window.POMODORO_SONGS || [];
  var musicPlayer = new musicPlayer_default({
    audio: document.getElementById("audio"),
    playBtn: document.getElementById("play"),
    prevBtn: document.getElementById("prev"),
    nextBtn: document.getElementById("next"),
    progress: document.getElementById("progress"),
    progressContainer: document.getElementById("progress-container"),
    cover: document.getElementById("cover"),
    musicTitle: document.getElementById("music-title"),
    songs
  });
  window.pomodoroApp = {
    timer,
    musicPlayer
  };
})();
