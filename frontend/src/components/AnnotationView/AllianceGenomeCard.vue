<template>
    <div class="card">
        <div class="card-base">
            <div class="card-header" v-html="modelName" />
            <div class="card-sub-header" v-html="modelBackground" />
            <div class="card-content">
                <div class="card-section" :style="associatedHumanDiseasesStyle"> Associated Human Diseases </div>
                <li class="card-list" v-for="(diseaseModel) in this.model.diseaseModels">
                    {{ diseaseModel.diseaseModel }}
                </li>
                <div class="card-section" :style="associatedPhenotypesStyle"> Associated Phenotypes </div>
                <div class="card-list"
                    v-for="(value, key) in this.associatedPhenotypesData"
                >
                    <b>{{ key }}</b>
                    <li v-for="item in value"> {{ item }}</li>
                </div>
                <div class="card-source">
                    <b>Source:</b> {{ this.model.source.name }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default ({
    name: 'alliance-genome-card',
    props: {
        model: {
            type: Object,
            default() {
                return {}
            }
        }
    },
    data() {
        return {
            frequentTerms: ['normal', 'abnormal', 'decreased', 'increased'],
            testObject: {
                'normal': ["hello", "goodbye", "hellogoodbye"],
                'abnormal': ["hello", "goodbye", "hellogoodbye"],
                'decreased': ["hello", "goodbye", "hellogoodbye"]
            },
            associatedHumanDiseasesData: {},
            associatedPhenotypesData: {}
        }
    },
    created() {
        this.calculateAssociatedPhenotypes();
        this.calculateAssociatedHumanDiseases();
    },
    computed: {
        modelName() {
            const regex = new RegExp('^(.*?)(?= \\[)', 'g');
            
            return this.model.name.match(regex)[0];
        },
        modelBackground() {
            let regex = new RegExp('\\[background:\]?(.*)', 'g');
            
            return this.model.name.match(regex)[0];
        },
        associatedHumanDiseasesStyle() {
            if(Object.keys(this.associatedHumanDiseasesData).length === 0)
                return {color: `var(--rosalution-grey-300)`};

            return 'color: black';
        },
        associatedPhenotypesStyle() {
            if(Object.keys(this.associatedPhenotypesData).length === 0)
                return {color: `var(--rosalution-grey-300)`};

            return 'color: black';
        }
    },
    methods: {
        calculateAssociatedHumanDiseases() {
            this.associatedHumanDiseasesData = this.model.diseaseModels;
        },
        calculateAssociatedPhenotypes() {
            let phenotypesDict = {'': [...this.model.phenotypes]};

            this.frequentTerms.forEach((term) => {
                phenotypesDict[term] = []
            })

            this.model.phenotypes.forEach((phenotype) => {
                this.frequentTerms.forEach((term) => {
                    
                    let regex = new RegExp('\\b' + term + '\\b', 'i');
                    
                    if(phenotype.match(regex)) {
                        phenotypesDict[term].push(phenotype);
                        phenotypesDict[''].splice(phenotypesDict[''].indexOf(phenotype), 1);
                    }
                })
            })

            Object.keys(phenotypesDict).forEach((key) => {
                if (phenotypesDict.hasOwnProperty(key) && !phenotypesDict[key].length) {
                    delete phenotypesDict[key];
                }
            })
            
            this.associatedPhenotypesData = phenotypesDict
        }
    }
});

</script>

<style scoped>

div {
  font-family: "Proxima Nova", sans-serif;
}

li {
    padding-top: 1%;
    padding-left: 4%;
    font-size: 15px;
}

.card {
    position: relative;
    text-decoration: none;
}

.card-header {
    font-size: 22px;
    font-weight: bold;
}

.card-sub-header {
    font-size: 16px;
    padding-top: 2%;
}

.card-base {
    width: 25rem;
    padding: var(--p-8);
    background-color: var(--rosalution-grey-50);
    display: block;
    box-sizing: border-box;
    color: inherit;
    position: relative;
    border-radius: var(--content-border-radius);
    height: 100%;
}

.card-content {
    padding-bottom: 10%;
}

.card-section {
    font-weight: bold;
    padding-top: 2.5%;
}

.card-list {
    padding-top: 1%;
    padding-left: 5%;
    font-size: 16px;
}

.card-source {
    position: absolute;
    bottom: 10px;
}

</style>