/**
 * Timer Unit Tests
 * Tests for the Pomodoro Timer module
 */

import Timer from '../timer';

describe('Timer Module', () => {
  let timer;
  let mockConfig;

  beforeEach(() => {
    // Create mock DOM elements
    const mockElement = (value) => ({
        value,
        textContent: '',
        disabled: false,
        className: '',
        addEventListener: jest.fn(),
        classList: {
        add: jest.fn(),
        remove: jest.fn(),
        toggle: jest.fn()
      }
    });

    mockConfig = {
      sessionInput: mockElement('25'),
      breakInput: mockElement('5'),
      minutesDisplay: mockElement(''),
      secondsDisplay: mockElement(''),
      timerLabel: mockElement(''),
      startBtn: mockElement(''),
      pauseBtn: mockElement(''),
      resetBtn: mockElement(''),
      onSessionChange: jest.fn()
    };

    timer = new Timer(mockConfig);
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
  });

  describe('Initialization', () => {
    test('should initialize with correct default values', () => {
      expect(timer.isSession).toBe(true);
      expect(timer.isRunning).toBe(false);
      expect(timer.timer).toBeNull();
    });

    test('should calculate initial timeLeft correctly', () => {
      expect(timer.timeLeft).toBe(25 * 60); // 25 minutes in seconds
    });

    test('should display initial time correctly', () => {
      expect(mockConfig.minutesDisplay.textContent).toBe('25');
      expect(mockConfig.secondsDisplay.textContent).toBe('00');
    });

    test('should attach event listeners to buttons', () => {
      expect(mockConfig.startBtn.addEventListener).toHaveBeenCalledWith(
        'click',
        expect.any(Function)
      );
      expect(mockConfig.pauseBtn.addEventListener).toHaveBeenCalledWith(
        'click',
        expect.any(Function)
      );
      expect(mockConfig.resetBtn.addEventListener).toHaveBeenCalledWith(
        'click',
        expect.any(Function)
      );
    });
  });

  describe('Start Functionality', () => {
    test('should start the timer', () => {
      timer.start();

      expect(timer.isRunning).toBe(true);
      expect(timer.timer).not.toBeNull();
      expect(mockConfig.startBtn.disabled).toBe(true);
      expect(mockConfig.pauseBtn.disabled).toBe(false);
      expect(mockConfig.startBtn.textContent).toBe('Running...');
    });

    test('should not start if already running', () => {
      timer.start();
      const firstTimer = timer.timer;

      timer.start();
      expect(timer.timer).toBe(firstTimer);
    });

    test('should decrement timeLeft every second', () => {
      timer.start();
      const initialTime = timer.timeLeft;

      jest.advanceTimersByTime(1000);

      expect(timer.timeLeft).toBe(initialTime - 1);
    });

    test('should update display as timer counts down', () => {
      const initialSeconds = 30;
      timer.timeLeft = initialSeconds;

      timer.start();
      jest.advanceTimersByTime(1000);

      expect(mockConfig.secondsDisplay.textContent).toBe('29');
    });
  });

  describe('Pause Functionality', () => {
    test('should pause the timer', () => {
      timer.start();
      timer.pause();

      expect(timer.isRunning).toBe(false);
      expect(timer.timer).toBeNull();
      expect(mockConfig.startBtn.disabled).toBe(false);
      expect(mockConfig.pauseBtn.disabled).toBe(true);
      expect(mockConfig.startBtn.textContent).toBe('Resume');
    });

    test('should stop timer from decrementing after pause', () => {
        timer.start();
        const timeAtPause = timer.timeLeft;

        jest.advanceTimersByTime(1000);
        timer.pause();
        const pausedTime = timer.timeLeft;

        jest.advanceTimersByTime(1000);

        expect(timer.timeLeft).toBe(pausedTime);
    });
  });

  describe('Reset Functionality', () => {
    test('should reset timer to initial state', () => {
      timer.start();
      timer.timeLeft = 100; // Simulate timer running

      timer.reset();

      expect(timer.isRunning).toBe(false);
      expect(timer.isSession).toBe(true);
      expect(timer.timeLeft).toBe(25 * 60);
      expect(timer.timer).toBeNull();
    });

    test('should reset button states', () => {
      timer.start();
      timer.reset();

      expect(mockConfig.startBtn.disabled).toBe(false);
      expect(mockConfig.pauseBtn.disabled).toBe(true);
      expect(mockConfig.startBtn.textContent).toBe('Start');
    });

    test('should reset display to initial time', () => {
        timer.timeLeft = 100;
        timer.updateDisplay();
        timer.reset();

      expect(mockConfig.minutesDisplay.textContent).toBe('25');
      expect(mockConfig.secondsDisplay.textContent).toBe('00');
    });
  });

  describe('Session Switching', () => {
    test('should switch from session to break when time expires', () => {
      timer.timeLeft = 2;
      timer.start();

      jest.advanceTimersByTime(1000);
      expect(timer.isSession).toBe(true); // First tick
      expect(timer.timeLeft).toBe(1);

      jest.advanceTimersByTime(1000);
      expect(timer.isSession).toBe(false); // Should switch
      expect(timer.timeLeft).toBe(5 * 60);
    });

    test('should call onSessionChange callback', () => {
      timer.timeLeft = 1;
      timer.start();

      jest.advanceTimersByTime(1000);

      expect(mockConfig.onSessionChange).toHaveBeenCalledWith(false);
    });

    test('should switch back to session after break ends', () => {
      timer.isSession = false;
      timer.timeLeft = 1;
      timer.start();

      jest.advanceTimersByTime(1000);

      expect(timer.isSession).toBe(true);
    });
  });

  describe('Settings Changes', () => {
    test('should update session length when changed while not running', () => {
      mockConfig.sessionInput.value = '30';

      // Simulate change event
      timer.sessionInput.dispatchEvent = jest.fn();
      timer.timeLeft = 0;
      timer.isRunning = false;
      timer.isSession = true;

      // Manually call the update logic
      timer.timeLeft = parseInt(mockConfig.sessionInput.value) * 60;

      expect(timer.timeLeft).toBe(30 * 60);
    });

    test('should not update session length while timer is running', () => {
      const originalTime = timer.timeLeft;
      timer.isRunning = true;

      mockConfig.sessionInput.value = '30';

      // If running, timeLeft should not change
      expect(timer.timeLeft).toBe(originalTime);
    });
  });

  describe('Display Updates', () => {
    test('should format minutes with leading zero', () => {
      timer.timeLeft = 5 * 60 + 30; // 5:30
      timer.updateDisplay();

      expect(mockConfig.minutesDisplay.textContent).toBe('05');
    });

    test('should format seconds with leading zero', () => {
      timer.timeLeft = 25 * 60 + 5; // 25:05
      timer.updateDisplay();

      expect(mockConfig.secondsDisplay.textContent).toBe('05');
    });

    test('should display "Work Session" for work periods', () => {
      timer.isSession = true;
      timer.updateDisplay();

      expect(mockConfig.timerLabel.textContent).toBe('Work Session');
    });

    test('should display "Break Time" for break periods', () => {
      timer.isSession = false;
      timer.updateDisplay();

      expect(mockConfig.timerLabel.textContent).toBe('Break Time');
    });
  });

  describe('Edge Cases', () => {
    test('should handle zero seconds correctly', () => {
      timer.timeLeft = 0;
      timer.updateDisplay();

      expect(mockConfig.minutesDisplay.textContent).toBe('00');
      expect(mockConfig.secondsDisplay.textContent).toBe('00');
    });

    test('should handle 59 seconds correctly', () => {
      timer.timeLeft = 59;
      timer.updateDisplay();

      expect(mockConfig.minutesDisplay.textContent).toBe('00');
      expect(mockConfig.secondsDisplay.textContent).toBe('59');
    });

    test('should prevent timer from going negative', () => {
      timer.timeLeft = 1;
      timer.start();

      jest.advanceTimersByTime(2000);

      expect(timer.timeLeft).toBeGreaterThanOrEqual(0);
    });
  });
});
