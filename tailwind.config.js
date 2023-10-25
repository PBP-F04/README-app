/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/*.html', './*/templates/*.html'],
  theme: {
      extend: {
        fontFamily: {
            Inter : ['Inter'],
            InterBold : ['InterBold']
        }
      },
    },
    plugins: [],
}

