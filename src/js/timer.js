/**
 * Timer Module - Manages the Pomodoro/Workout timer functionality
 * Handles work sessions and break periods with automatic switching
 */

class Timer {
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
    this.startBtn.addEventListener('click', () => this.start());
    this.pauseBtn.addEventListener('click', () => this.pause());
    this.resetBtn.addEventListener('click', () => this.reset());

    this.sessionInput.addEventListener('change', () => {
      if (!this.isRunning) {
        this.timeLeft = parseInt(this.sessionInput.value) * 60;
        this.updateDisplay();
      }
    });

    this.breakInput.addEventListener('change', () => {
      if (!this.isRunning && !this.isSession) {
        this.timeLeft = parseInt(this.breakInput.value) * 60;
        this.updateDisplay();
      }
    });
  }

  updateDisplay() {
    const min = String(Math.floor(this.timeLeft / 60)).padStart(2, '0');
    const sec = String(this.timeLeft % 60).padStart(2, '0');
    this.minutesDisplay.textContent = min;
    this.secondsDisplay.textContent = sec;
    this.timerLabel.textContent = this.isSession ? 'Work Session' : 'Break Time';
  }

  start() {
    if (this.timer) return;

    this.isRunning = true;
    this.startBtn.disabled = true;
    this.pauseBtn.disabled = false;
    this.startBtn.textContent = 'Running...';

    this.timer = setInterval(() => {
      this.timeLeft--;
      this.updateDisplay();

      if (this.timeLeft <= 0) {
        this.switchSession();
      }
    }, 1000);
  }

  switchSession() {
    this.isSession = !this.isSession;
    this.timeLeft = (this.isSession ? parseInt(this.sessionInput.value) : parseInt(this.breakInput.value)) * 60;
    this.updateDisplay();

    // Trigger callback when session changes (for audio notification)
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
    this.startBtn.textContent = 'Resume';
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
    this.startBtn.textContent = 'Start';
  }
}

export default Timer;
