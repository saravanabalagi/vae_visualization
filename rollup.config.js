import svelte from 'rollup-plugin-svelte';
import resolve from '@rollup/plugin-node-resolve';
import globals from "rollup-plugin-node-globals";
import builtins from "rollup-plugin-node-builtins";
import commonjs from '@rollup/plugin-commonjs';
import livereload from 'rollup-plugin-livereload';
import { terser } from 'rollup-plugin-terser';
import preprocess from 'svelte-preprocess';
import postcss from 'rollup-plugin-postcss';
import alias from '@rollup/plugin-alias';
import path from 'path';

const production = !process.env.ROLLUP_WATCH;
const projectRootDir = path.resolve(__dirname);


function serve() {
	let server;

	function toExit() {
		if (server) server.kill(0);
	}

	return {
		writeBundle() {
			if (server) return;
			server = require('child_process').spawn('npm', ['run', 'start', '--', '--dev'], {
				stdio: ['ignore', 'inherit', 'inherit'],
				shell: true
			});

			process.on('SIGTERM', toExit);
			process.on('exit', toExit);
		}
	};
}

export default {
	input: 'src/main.js',
	output: {
		sourcemap: true,
		format: 'iife',
		name: 'app',
		file: 'public/build/bundle.js'
	},
	plugins: [
		svelte({
			// enable run-time checks when not in production
			dev: !production,
			// we'll extract any component CSS out into
			// a separate file - better for performance
			preprocess: preprocess(),
			css: css => {
				css.write('public/build/bundle.css');
			}
		}),

		alias({
			entries: [
			  { find: 'stores', replacement: path.resolve(projectRootDir, 'src', 'stores') }
			]
		}),

		// user defined
		postcss(),
		commonjs(),
		globals(),
		builtins(),
		
		// If you have external dependencies installed from
		// npm, you'll most likely need these plugins. In
		// some cases you'll need additional configuration -
		// consult the documentation for details:
		// https://github.com/rollup/plugins/tree/master/packages/commonjs
		resolve({
			browser: true,
			dedupe: ['svelte']
		}),

		// In dev mode, call `npm run start` once
		// the bundle has been generated
		!production && serve(),

		// Watch the `public` directory and refresh the
		// browser on changes when not in production
		!production && livereload('public'),

		// If we're building for production (npm run build
		// instead of npm run dev), minify
		production && terser()
	],
	watch: {
		clearScreen: false
	}
};
