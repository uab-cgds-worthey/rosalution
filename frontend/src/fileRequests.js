import Requests from '@/requests.js';

export default {
    async getImage(fileId) {
        const url = `/rosalution/api/analysis/download/${fileId}`;
        return await Requests.getImage(url);
    }
}