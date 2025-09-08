import {describe, expect, it} from 'vitest';

import { chooseAnimalModelsSchema } from '@/components/AnnotationView/allianceGenomeRenderingUtility';

import modelFixture from "../../__fixtures__/mockAllianceGenomeModels.json"

describe('allianceGenomeRenderingUtility.js', () => {
  it.each([
    ['aliance genome 8.1.0<=', modelFixture['8.1.0<=,LMNA,fish'], 'lmna<sup>bw25/bw25</sup>'],
    ['aliance genome 8.2.0>=', modelFixture['8.2.0>=,LMNA,fish'], 'lmna<sup>bw25/bw25</sup>']
  ])('Should %s return an animal model name', (title, mockModel, expected) => {
    const actualModel = chooseAnimalModelsSchema(mockModel)
    expect('name' in actualModel).to.equal(true);
    expect(actualModel.name).to.include(expected)
  });

  it.each([
    ['aliance genome 8.1.0<=', modelFixture['8.1.0<=,LMNA,fish'], true, 'lmna<sup>bw25/bw25</sup> [background:] involves: 129S4/SvJae * C57BL/6'],
    ['aliance genome 8.2.0>=', modelFixture['8.2.0>=,LMNA,fish'], true, 'lmna<sup>bw25/bw25</sup>'],
    ['alliance genome 8.2.0>=', modelFixture['8.2.0>=,NUMB,mouse'], true, 'Numb<sup>tm1Zili</sup>/Numb<sup>tm1Zili</sup> Numbl<sup>tm1Zili</sup>/Numbl<sup>tm1Zili</sup> Tg(Mx1-cre)1Cgn/?  [background:] involves: 129/Sv * C57BL/6 * CBA']
  ])('Should %s return model background', (title, mockModel,expectedExist, expected) => {
    const actualModel = chooseAnimalModelsSchema(mockModel)
    expect('background' in actualModel).to.equal(expectedExist);
    expect(actualModel?.background).to.equal(expected)
  });

  it.each([
    ['aliance genome 8.1.0<=', modelFixture['8.1.0<=,LMNA,fish'], 'ZFIN'],
    ['aliance genome 8.2.0>=', modelFixture['8.2.0>=,LMNA,fish'], 'ZFIN']
  ])('Should %s return a model provider', (title, mockModel, expected) => {
    const actualModel = chooseAnimalModelsSchema(mockModel)
    expect('source' in actualModel).to.equal(true);
    expect(actualModel.source).to.include(expected)
  });
    [

]
  it.each([
    ['aliance genome 8.1.0<=', modelFixture['8.1.0<=,LMNA,fish']],
    ['aliance genome 8.2.0>=', modelFixture['8.2.0>=,LMNA,fish']]
  ])('Should %s return phenotypes', (title, mockModel) => {
    const actualModel = chooseAnimalModelsSchema(mockModel)
    expect('phenotypes' in actualModel).to.equal(true);

    expect(actualModel.phenotypes).to.include.members([
        "heart contraction decreased rate, abnormal",
        "heart decreased functionality, abnormal",
        "atrioventricular canal cardiac conduction decreased process quality, abnormal",
        "cardiac muscle cell nucleus morphology, abnormal",
        "cardiac ventricle cardiac conduction decreased process quality, abnormal",
    ])
  });

  it('should handle missing experimental conditions for aliance genome 8.1.0 schema', () => {
    const actualModel = chooseAnimalModelsSchema(modelFixture['8.1.0<=,NUMB,mouse']);
    expect('conditions' in actualModel).to.equal(false)
  })

it.each([
    ['aliance genome 8.1.0<=', modelFixture['8.1.0<=,LMNA,fish'], true, ['progeria', 'otitis media']],
    ['aliance genome 8.2.0>=', modelFixture['8.2.0>=,LMNA,fish'], false, []]
  ])('Should %s return disease models', (title, mockModel,expectedExist, expected) => {
    const actualModel = chooseAnimalModelsSchema(mockModel)
    expect('diseaseModels' in actualModel).to.equal(expectedExist);

    expected.forEach((expectedDisease) => {
        const actualDisease = actualModel?.diseaseModels.map(disease => disease.diseaseModel);
        expect(actualDisease).to.include(expectedDisease)
    })
  });

it.each([
    ['aliance genome 8.1.0<=', modelFixture['8.1.0<=,LMNA,fish'], true, 1, 'standard conditions'],
    ['aliance genome 8.2.0>=', modelFixture['8.2.0>=,LMNA,fish'], true, 1, 'standard conditions']
  ])('Should %s return experimental conditions', (title, mockModel,expectedExist, expectedLength, expected) => {
    const actualModel = chooseAnimalModelsSchema(mockModel)
    expect('conditions' in actualModel).to.equal(expectedExist);

    expect(actualModel.conditions).to.have.lengthOf(expectedLength)
    actualModel['conditions'].forEach((condition) => {
        expect(condition).to.have.property('conditionStatement', expected)
    })
  });
});
