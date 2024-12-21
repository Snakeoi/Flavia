export default (regex, length) => {
    const charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_-+=<>?/';
    let password = '';

    const getRandomChar = () => charset[Math.floor(Math.random() * charset.length)];

    while (!regex.test(password)) {
        password = Array.from({ length: length }, getRandomChar).join('');
    }

    return password;
}