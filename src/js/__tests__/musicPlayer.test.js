/**
 * MusicPlayer Unit Tests
 * Tests for the Music Player module
 */

import MusicPlayer from '../musicPlayer';

describe('MusicPlayer Module', () => {
  let musicPlayer;
  let mockConfig;

  beforeEach(() => {
    // Create mock DOM elements
    const mockIcon = {
      classList: {
        add: jest.fn(),
        remove: jest.fn()
      }
    };

    const mockElement = (isButton = false) => {
      const el = {
        textContent: '',
        src: '',
        style: {},
        clientWidth: 400,
        addEventListener: jest.fn(),
        classList: {
          add: jest.fn(),
          remove: jest.fn(),
          toggle: jest.fn(),
          contains: jest.fn()
        }
      };

      if (isButton) {
        el.querySelector = jest.fn(() => mockIcon);
      }

      return el;
    };

    mockConfig = {
      audio: mockElement(),
      playBtn: mockElement(true),
      prevBtn: mockElement(true),
      nextBtn: mockElement(true),
      progress: mockElement(),
      progressContainer: mockElement(),
      cover: mockElement(),
      musicTitle: mockElement(),
      songs: [
        { title: 'Song 1', src: '/music/song1.mp3', cover: '/img/cover1.jpg' },
        { title: 'Song 2', src: '/music/song2.mp3', cover: '/img/cover2.jpg' },
        { title: 'Song 3', src: '/music/song3.mp3', cover: '/img/cover3.jpg' }
      ]
    };

    // Mock audio methods
    mockConfig.audio.play = jest.fn().mockResolvedValue(undefined);
    mockConfig.audio.pause = jest.fn();
    mockConfig.audio.duration = 0;
    mockConfig.audio.currentTime = 0;

    musicPlayer = new MusicPlayer(mockConfig);
  });

  describe('Initialization', () => {
    test('should initialize with correct default values', () => {
      expect(musicPlayer.isPlaying).toBe(false);
      expect(musicPlayer.currentSongIndex).toBe(0);
    });

    test('should load first song on init', () => {
      expect(mockConfig.audio.src).toBe('/music/song1.mp3');
      expect(mockConfig.cover.src).toBe('/img/cover1.jpg');
      expect(mockConfig.musicTitle.textContent).toBe('Song 1');
    });

    test('should attach event listeners', () => {
      expect(mockConfig.playBtn.addEventListener).toHaveBeenCalled();
      expect(mockConfig.prevBtn.addEventListener).toHaveBeenCalled();
      expect(mockConfig.nextBtn.addEventListener).toHaveBeenCalled();
      expect(mockConfig.audio.addEventListener).toHaveBeenCalled();
      expect(mockConfig.progressContainer.addEventListener).toHaveBeenCalled();
    });
  });

  describe('Play Functionality', () => {
    test('should set isPlaying to true', () => {
      musicPlayer.play();

      expect(musicPlayer.isPlaying).toBe(true);
    });

    test('should call audio play method', () => {
      musicPlayer.play();

      expect(mockConfig.audio.play).toHaveBeenCalled();
    });

    test('should update play button visual state', () => {
      musicPlayer.play();

      expect(mockConfig.playBtn.classList.add).toHaveBeenCalledWith('playing');
    });

    test('should update play button icon', () => {
      musicPlayer.play();

      const icon = mockConfig.playBtn.querySelector('i');
      expect(icon.classList.remove).toHaveBeenCalledWith('fa-play');
      expect(icon.classList.add).toHaveBeenCalledWith('fa-pause');
    });

    test('should handle play errors gracefully', async () => {
      mockConfig.audio.play = jest.fn().mockRejectedValue(new Error('Play failed'));
      musicPlayer.audio = mockConfig.audio;

      // The actual code catches the error, so we just verify it doesn't throw
      expect(() => musicPlayer.play()).not.toThrow();
    });
  });

  describe('Pause Functionality', () => {
    test('should set isPlaying to false', () => {
      musicPlayer.isPlaying = true;
      musicPlayer.pause();

      expect(musicPlayer.isPlaying).toBe(false);
    });

    test('should call audio pause method', () => {
      musicPlayer.pause();

      expect(mockConfig.audio.pause).toHaveBeenCalled();
    });

    test('should update play button visual state', () => {
      musicPlayer.isPlaying = true;
      musicPlayer.pause();

      expect(mockConfig.playBtn.classList.remove).toHaveBeenCalledWith('playing');
    });

    test('should update play button icon', () => {
      musicPlayer.isPlaying = true;
      musicPlayer.pause();

      const icon = mockConfig.playBtn.querySelector();
      expect(icon.classList.add).toHaveBeenCalledWith('fa-play');
      expect(icon.classList.remove).toHaveBeenCalledWith('fa-pause');
    });
  });

  describe('Toggle Play', () => {
    test('should play if not playing', () => {
      musicPlayer.isPlaying = false;
      jest.spyOn(musicPlayer, 'play');

      musicPlayer.togglePlay();

      expect(musicPlayer.play).toHaveBeenCalled();
    });

    test('should pause if playing', () => {
      musicPlayer.isPlaying = true;
      jest.spyOn(musicPlayer, 'pause');

      musicPlayer.togglePlay();

      expect(musicPlayer.pause).toHaveBeenCalled();
    });
  });

  describe('Navigation', () => {
    test('should load next song', () => {
      expect(musicPlayer.currentSongIndex).toBe(0);

      musicPlayer.nextSong();

      expect(musicPlayer.currentSongIndex).toBe(1);
      expect(mockConfig.audio.src).toBe('/music/song2.mp3');
      expect(mockConfig.musicTitle.textContent).toBe('Song 2');
    });

    test('should loop to first song after last', () => {
      musicPlayer.currentSongIndex = 2;

      musicPlayer.nextSong();

      expect(musicPlayer.currentSongIndex).toBe(0);
      expect(mockConfig.audio.src).toBe('/music/song1.mp3');
    });

    test('should load previous song', () => {
      musicPlayer.currentSongIndex = 1;

      musicPlayer.prevSong();

      expect(musicPlayer.currentSongIndex).toBe(0);
      expect(mockConfig.audio.src).toBe('/music/song1.mp3');
    });

    test('should loop to last song when prev at first', () => {
      musicPlayer.currentSongIndex = 0;

      musicPlayer.prevSong();

      expect(musicPlayer.currentSongIndex).toBe(2);
      expect(mockConfig.audio.src).toBe('/music/song3.mp3');
    });

    test('should auto-play when navigating if already playing', () => {
      musicPlayer.isPlaying = true;
      jest.spyOn(musicPlayer, 'play');

      musicPlayer.nextSong();

      expect(musicPlayer.play).toHaveBeenCalled();
    });

    test('should not auto-play when navigating if paused', () => {
      musicPlayer.isPlaying = false;
      jest.spyOn(musicPlayer, 'play');

      musicPlayer.nextSong();

      expect(musicPlayer.play).not.toHaveBeenCalled();
    });
  });

  describe('Progress Bar', () => {
    test('should update progress bar on timeupdate', () => {
      mockConfig.audio.duration = 100;
      mockConfig.audio.currentTime = 50;

      musicPlayer.updateProgress();

      expect(mockConfig.progress.style.width).toBe('50%');
    });

    test('should handle zero duration gracefully', () => {
      mockConfig.audio.duration = 0;
      mockConfig.audio.currentTime = 0;

      musicPlayer.updateProgress();

      expect(mockConfig.progress.style.width).toBe('0%');
    });

    test('should seek to clicked position', () => {
      mockConfig.audio.duration = 100;

      const mockEvent = {
        offsetX: 200
      };

      musicPlayer.setProgress(mockEvent);

      expect(mockConfig.audio.currentTime).toBe(50); // 200/400 * 100
    });

    test('should handle seek at different positions', () => {
      mockConfig.audio.duration = 60;

      const mockEvent = {
        offsetX: 100 // 1/4 of container width
      };

      musicPlayer.setProgress(mockEvent);

      expect(mockConfig.audio.currentTime).toBe(15); // 1/4 of 60 seconds
    });
  });

  describe('Load Song', () => {
    test('should load song with valid index', () => {
      musicPlayer.loadSong(2);

      expect(mockConfig.audio.src).toBe('/music/song3.mp3');
      expect(mockConfig.cover.src).toBe('/img/cover3.jpg');
      expect(mockConfig.musicTitle.textContent).toBe('Song 3');
    });

    test('should not load song with invalid index', () => {
      const originalSrc = mockConfig.audio.src;

      musicPlayer.loadSong(10);

      expect(mockConfig.audio.src).toBe(originalSrc);
    });

    test('should update currentSongIndex', () => {
      musicPlayer.loadSong(1);

      expect(musicPlayer.currentSongIndex).toBe(1);
    });
  });

  describe('Empty Playlist', () => {
    test('should handle empty songs array', () => {
      const emptyConfig = { ...mockConfig, songs: [] };
      const emptyPlayer = new MusicPlayer(emptyConfig);

      expect(emptyPlayer.songs.length).toBe(0);
    });

    test('should not crash on navigation with empty playlist', () => {
      musicPlayer.songs = [];

      expect(() => musicPlayer.nextSong()).not.toThrow();
    });
  });

  describe('Edge Cases', () => {
    test('should handle progress bar click at start', () => {
      mockConfig.audio.duration = 100;

      const mockEvent = { offsetX: 0 };

      musicPlayer.setProgress(mockEvent);

      expect(mockConfig.audio.currentTime).toBe(0);
    });

    test('should handle progress bar click at end', () => {
      mockConfig.audio.duration = 100;

      const mockEvent = { offsetX: 400 }; // Full width

      musicPlayer.setProgress(mockEvent);

      expect(mockConfig.audio.currentTime).toBe(100);
    });

    test('should handle rapid song changes', () => {
      musicPlayer.nextSong();
      musicPlayer.nextSong();
      musicPlayer.prevSong();

      expect(musicPlayer.currentSongIndex).toBe(1);
    });
  });
});
