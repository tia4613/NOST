import create from 'zustand';

const useThemeStore = create(set => ({
    isDarkMode: false,
    isThemeMode: false,
    toggleDarkMode: () => set(state => ({ isDarkMode: !state.isDarkMode })),
    toggleThemeMode: () => set(state => ({ isThemeMode: !state.isThemeMode })),
    themes: {
        spring: {
            primary: '#ff7f7f',
            secondary: '#ffeef8',
            textColor: '#305030',
            fontFamily: 'Georgia',
            sidebarBg: '#f8b7d0',
            additionalColors: ['#ffcad4', '#f4acb7', '#9d8189', '#d8e2dc', '#8d99ae'],
            backgroundImage: 'url("https://images.unsplash.com/photo-1491466424936-e304919aada7?q=80&w=1738&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")',
            buttonBackgroundColor: '#ff7f7f',
            buttonTextColor: '#ffeef8'

        },
        summer: {
            primary: '#0af',
            secondary: '#a1c4fd',
            textColor: '#001f3f',
            fontFamily: 'Verdana',
            sidebarBg: '#7ec8e3',
            additionalColors: ['#3bceac', '#5cdb95', '#379683', '#8ee4af', '#05386b'],
            backgroundImage: 'url("https://images.unsplash.com/photo-1491466424936-e304919aada7?q=80&w=1738&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")',
            buttonBackgroundColor: '#0af',
            buttonTextColor: '#a1c4fd'

        },
        autumn: {
            primary: '#fa8231',
            secondary: '#f7c978',
            textColor: '#561212',
            fontFamily: 'Times New Roman',
            sidebarBg: '#d49a6a',
            additionalColors: ['#ed6663', '#ffa372', '#b27749', '#f7b32b', '#eae8e1'],
            backgroundImage: 'url("https://images.unsplash.com/photo-1491466424936-e304919aada7?q=80&w=1738&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")',
            buttonBackgroundColor: '#fa8231',
            buttonTextColor: '#f7c978'
        },
        winter: {
            primary: '#80d0c7',
            secondary: '#91d1e3',
            textColor: '#f5f5f5',
            fontFamily: 'Courier New',
            sidebarBg: '#5eaaa8',
            additionalColors: ['#bcf8ec', '#a9def9', '#e4bad4', '#f1e3f3', '#ceb5b7'],
            backgroundImage: 'url("https://images.unsplash.com/photo-1491466424936-e304919aada7?q=80&w=1738&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")',
            buttonBackgroundColor: '#80d0c7',
            buttonTextColor: '#f5f5f5'
        }
    }
}));

export default useThemeStore;