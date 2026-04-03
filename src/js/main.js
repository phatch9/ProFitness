/**
 * Main Entry Point - Initializes the Pomodoro Timer application
 * Combines Timer and MusicPlayer modules
 */

import Timer from './timer.js';
import MusicPlayer from './musicPlayer.js';

// Initialize Timer
const timer = new Timer({
    sessionInput: document.getElementById('session-length'),
    breakInput: document.getElementById('break-length'),
    minutesDisplay: document.getElementById('minutes'),
    secondsDisplay: document.getElementById('seconds'),
    timerLabel: document.getElementById('timer-label'),
    startBtn: document.getElementById('start'),
    pauseBtn: document.getElementById('pause'),
    resetBtn: document.getElementById('reset'),
    onSessionChange: (isSession) => {
    // Play notification sound when session changes
    if (musicPlayer && musicPlayer.audio && musicPlayer.audio.readyState >= 2) {
      musicPlayer.audio.play().catch(e => console.log('Audio play failed:', e));
    }
  }
});

// Initialize Music Player with songs
// Note: Song paths are injected by Flask template (see pomodoroTimer.html)
const songs = window.POMODORO_SONGS || [];

const musicPlayer = new MusicPlayer({
  audio: document.getElementById('audio'),
  playBtn: document.getElementById('play'),
  prevBtn: document.getElementById('prev'),
  nextBtn: document.getElementById('next'),
  progress: document.getElementById('progress'),
  progressContainer: document.getElementById('progress-container'),
  cover: document.getElementById('cover'),
  musicTitle: document.getElementById('music-title'),
  songs: songs
});

// Expose globally for debugging
window.pomodoroApp = {
  timer,
  musicPlayer
};
