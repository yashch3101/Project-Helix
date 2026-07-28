import { storage } from "./storage";

export const auth = {

    getToken() {
        return storage.getToken();
    },

    saveToken(token: string) {
        storage.setToken(token);
    },

    logout() {
        storage.removeToken();
    },

    isAuthenticated() {
        return !!storage.getToken();
    },

};