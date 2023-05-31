<template>
    <div class="card">
        <div class="card-base">
            <div class="card-header" v-html="modelName" data-test="model-header"/>
            <div class="card-sub-header" v-html="modelBackground" data-test="model-background"/>
            <div class="card-content">
                <div class="card-section" :style="experimentalConditionStyle" data-test="model-section-condition">
                    Experimental Condition
                </div>
                <li class="card-list"
                    v-for="condition in this.experimentalConditions"
                    data-test="model-list-condition"
                >
                {{ condition.conditionStatement }}
                </li>
                <div class="card-section" :style="associatedHumanDiseasesStyle" data-test="model-section-disease">
                    Associated Human Diseases
                </div>
                <li class="card-list" v-for="(diseaseModel) in this.model.diseaseModels" data-test="model-list-disease">
                    {{ diseaseModel.diseaseModel }}
                </li>
                <div class="card-section" :style="associatedPhenotypesStyle" data-test="model-section-phenotype">
                    Associated Phenotypes
                </div>
                <div class="card-list"
                    v-for="(value, key) in this.associatedPhenotypesData"
                    data-test="model-list-phenotype"
                >
                <div v-if="key != ''">
                    <font-awesome-icon v-if="value.icon" :icon="value.icon" :style="value.iconStyle"/>
                    <span class="card-section-term" :style="value.style">{{ key }}</span>
                </div>
                    <ul>
                        <li v-for="item in value.phenotypes">{{ item }}</li>
                    </ul>
                </div>
                <div class="card-source" data-test="model-source">
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
        return {};
      },
    },
  },
  data() {
    return {
      // Note: Consolidate these into a single object, there's no need to update two places for a frequent term.
      frequentTerms: ['normal', 'abnormal', 'absent', 'increased', 'decreased'],
      frequentTermsObject: [
        {
          term: 'normal',
          style: {'color': 'var(--rosalution-purple-300)'},
          icon: '',
          iconStyle: {},
        },
        {
          term: 'abnormal',
          style: {'color': 'var(--rosalution-red-100)'},
          icon: '',
          iconStyle: {},
        },
        {
          term: 'absent',
          style: {'color': 'var(--rosalution-red-100)'},
          icon: '',
          iconStyle: {},
        },
        {
          term: 'increased',
          style: {'color': 'var(--rosalution-purple-300)'},
          icon: 'arrow-up',
          iconStyle: {'color': 'purple'},
        },
        {
          term: 'decreased',
          style: {'color': 'var(--rosalution-red-100)'},
          icon: 'arrow-down',
          iconStyle: {'color': 'var(--rosalution-red-100)'},
        },
      ],
      associatedHumanDiseasesData: {},
      associatedPhenotypesData: {},
      experimentalConditions: {},
    };
  },
  created() {
    this.calculateExperimentalCondition();
    this.calculateAssociatedPhenotypes();
    this.calculateAssociatedHumanDiseases();
  },
  computed: {
    modelName() {
      const regex = new RegExp('^(.*?)(?= \\[)', 'g');
      const matchResult = this.model.name.match(regex);

      if (matchResult) {
        return matchResult[0];
      }

      return this.model.name;
    },
    modelBackground() {
      const regex = new RegExp('\\[background:\]?(.*)', 'g');

      const matchResult = this.model.name.match(regex);

      if (matchResult) {
        return matchResult[0];
      }

      return '';
    },
    associatedHumanDiseasesStyle() {
      if (Object.keys(this.associatedHumanDiseasesData).length === 0) {
        return {color: `var(--rosalution-grey-300)`};
      }

      return 'color: black';
    },
    associatedPhenotypesStyle() {
      if (Object.keys(this.associatedPhenotypesData).length === 0) {
        return {color: `var(--rosalution-grey-300)`};
      }

      return 'color: black';
    },
    experimentalConditionStyle() {
      if (Object.keys(this.experimentalConditions).length === 0) {
        return {color: `var(--rosalution-grey-300)`};
      }

      return 'color: black';
    },
  },
  methods: {
    calculateAssociatedHumanDiseases() {
      this.associatedHumanDiseasesData = this.model.diseaseModels;
    },
    calculateAssociatedPhenotypes() {
      const phenotypesDict = {'':
                {
                  phenotypes: [],
                  style: '',
                  icon: '',
                  iconStyle: {},
                },
      };

      this.model.phenotypes.forEach((phenotype) => {
        phenotypesDict[''].phenotypes.push(phenotype);
      });

      this.frequentTermsObject.forEach((term) => {
        phenotypesDict[term.term] = {
          phenotypes: [],
          style: term.style,
          icon: term.icon,
          iconStyle: term.iconStyle,
        };
      });

      this.model.phenotypes.forEach((phenotype) => {
        this.frequentTermsObject.forEach((term) => {
          const regex = new RegExp('\\b' + term.term + '\\b', 'i');

          if (phenotype.match(regex)) {
            phenotypesDict[term.term].phenotypes.push(phenotype);
            phenotypesDict[''].phenotypes.splice(phenotypesDict[''].phenotypes.indexOf(phenotype), 1);
          }
        });
      });

      Object.keys(phenotypesDict).forEach((key) => {
        if (phenotypesDict.hasOwnProperty(key) && !phenotypesDict[key].phenotypes.length) {
          delete phenotypesDict[key];
        }
      });

      this.associatedPhenotypesData = phenotypesDict;
    },
    calculateExperimentalCondition() {
      if (Object.keys(this.model.conditions).length == 0) {
        return;
      }

      this.experimentalConditions = this.model.conditions.has_condition;
    },
  },
});

</script>

<style scoped>

div {
  font-family: "Proxima Nova", sans-serif;
}

ul {
    list-style-type: disc;
    padding-left: 7%;
}

li {
    margin-left: 10px;
    padding-top: 1%;

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
    width: 30rem;
    padding: var(--p-8);
    background-color: var(--rosalution-grey-50);
    display: block;
    box-sizing: border-box;
    color: inherit;
    position: relative;
    border-radius: var(--content-border-radius);
    height: 35rem;
    overflow-y: scroll;
}

.card-content {
    padding-bottom: 10%;
}

.card-section {
    font-weight: bold;
    padding-top: 2.5%;
}

.card-section-term {
    padding-left: var(--p-5);
}

.card-list {
    padding-top: 1%;
    padding-left: 5%;
    font-size: 16px;
}

.card-source {
    overflow-y: scroll;
}

</style>