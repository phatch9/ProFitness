# ProFitness Development Build Guide

## JavaScript Build Setup

This project now uses **esbuild** for bundling modular JavaScript code.

### Project Structure

```
src/js/
  ├── main.js           # Entry point - initializes Timer and MusicPlayer
  ├── timer.js          # Timer module (Pomodoro timer functionality)
  └── musicPlayer.js    # Music player module

fitness/static/js/
  └── bundle.js         # Generated bundled file (do not edit)
```

### Installation

```bash
# Install dependencies (esbuild)
npm install
```

### Available Scripts

```bash
# Build for development
npm run build

# Watch mode - rebuilds on file changes (great for development)
npm run dev

# Build for production (minified)
npm run build:prod
```

### Development Workflow

1. **Make changes** to files in `src/js/`
2. **Run watch mode:**
   ```bash
   npm run dev
   ```
   This will automatically rebuild `fitness/static/js/bundle.js` whenever you save changes.
3. **Refresh** the browser to see updates

### Module System

The code now uses **ES6 modules**:

#### Timer Module (`timer.js`)
```javascript
import Timer from './timer.js';

const timer = new Timer({
  sessionInput: document.getElementById('session-length'),
  breakInput: document.getElementById('break-length'),
  // ... other config
});
```

#### Music Player Module (`musicPlayer.js`)
```javascript
import MusicPlayer from './musicPlayer.js';

const musicPlayer = new MusicPlayer({
  audio: document.getElementById('audio'),
  // ... other config
});
```

### Bundle Size

- **Development:** 7.2 KB (unminified)
- **Production:** ~3.5 KB (minified with `npm run build:prod`)

### Debugging

The Pomodoro app is exposed globally for debugging:

```javascript
// In browser console
window.pomodoroApp.timer
window.pomodoroApp.musicPlayer
```

### Benefits of This Setup

✅ **Modular Code** - Separated concerns (timer vs audio)  
✅ **Reusable** - Modules can be imported in other pages  
✅ **Maintainable** - Easy to locate and update features  
✅ **Testable** - Each class can be unit tested independently  
✅ **Fast Builds** - esbuild bundles in milliseconds  
✅ **Small Bundle** - Properly bundled and can be minified

### Next Steps

1. Extract music player and timer logic from other pages
2. Create shared utility modules for common functions
3. Add TypeScript (optional) for better type safety
4. Add unit tests with Jest
