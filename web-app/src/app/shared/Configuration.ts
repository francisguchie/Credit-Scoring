declare var window: any;

export const commonValues: any = {
    RESPONSE_SUCCESS_STATUS: '0000'
};

export const ENV_PATH: any = {
  //  DEV_URL: 'http://localhost:3000',
    SIT_URL: '',
    UAT_URL: '',
    DEV_URL: 'http://localhost:5000/',
};
// https://localhost:8443/fineract-provider/api/v1/helloworld?tenantIdentifier=default&Authorization=bWlmb3M6cGFzc3dvcmQ=
const SERVICE_URLS_MAP = {
    getAllFeatures : 'feature/getAllFeatures',
    saveFeature : 'feature/saveFeature?tenantIdentifier=default',
    getAllConfigs: 'config/getAllConfig',
    saveConfig : 'config/saveConfig',
    getOneCriteria : 'criteria/getByCriteriaId',
    getAllCriterias: 'criteria/getAllCriterias',
    saveCriteria : 'criteria/saveCriteria',
    getOneFeature: 'feature/getByFeatureId',
    getOneConfig: 'config/getByConfigId?tenantIdentifier=default',
    getFeatureCatgory: 'feature/featureNCategory',
    getScore: 'score/calc',
    getJsonScore: 'score/calc/json',
    getXmlScore: 'score/calc/xml',
    getStatScore: 'score/calc/stat',
    getMLScore: 'score/calc/ml',
    getRBScore: '/score/calc/sql',
    uploadCSV: 'upload/csv'

};

export class Config {

    public static getEnvironmentVariable(value) {
        let environment = window.location.hostname.match('(sit|dev|localhost)')[0];
        environment = environment === 'localhost' ? 'DEV' : environment;
        console.log(environment);
        console.log(ENV_PATH[environment + '_URL'] + SERVICE_URLS_MAP[value]);
        return ENV_PATH[environment + '_URL'] + SERVICE_URLS_MAP[value] + '?tenantIdentifier=default&Authorization=bWlmb3M6cGFzc3dvcmQ=';
    }
}
