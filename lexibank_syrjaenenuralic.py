from pathlib import Path
import lingpy as lp

from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank.util import getEvoBibAsBibtex
from pylexibank import progressbar
from pylexibank import Concept, Language
import attr

@attr.s
class CustomConcept(Concept):
    Number = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'syrjaenenuralic'
    concept_class = CustomConcept

    def cmd_makecldf(self, args):
    
        concepts = {}
        wl = lp.Wordlist(self.raw_dir.joinpath('D_test_Uralic-173-8.tsv').as_posix())

        for concept in self.conceptlists[0].concepts.values():
            idx = '{0}_{1}'.format(concept.number, slug(concept.english))
            args.writer.add_concept(
                    ID=idx,
                    Number=concept.number,
                    Name=concept.english,
                    Concepticon_ID=concept.concepticon_id,
                    Concepticon_Gloss=concept.concepticon_gloss,
                    )
            concepts[concept.english] = idx
        concepts['earth, soil'] = concepts['earth']
        concepts['person, human'] = concepts['person']
        concepts['fly'] = concepts['fly (v.)']
        concepts['meat (flesh)'] = concepts['meat, flesh']
        #concepts['burn'] = concepts['burn tr.']
        #concepts['claw'] = concepts['claw (nail)']
        #concepts['come (V)'] = concepts['come']
        #concepts['die (V)'] = concepts['die']
        #concepts['drink (V)'] = concepts['drink']
        #concepts['eat (V)'] = concepts['eat']
        #concepts['fat'] = concepts['fat n.']
        #concepts['fly'] = concepts['fly v.']
        #concepts['give (V)'] = concepts['give']
        #concepts['hear (V)'] = concepts['hear']
        #concepts['kill (V)'] = concepts['kill']
        #concepts['know (V)'] = concepts['know']
        #concepts['lie (V)'] = concepts['lie']
        #concepts['rain (V)'] = concepts['rain']
        #concepts['say (V)'] = concepts['say']
        #concepts['see (V)'] = concepts['see']
        #concepts['sit (V)'] = concepts['sit']
        #concepts['sleep (V)'] = concepts['sleep']
        #concepts['stand (V)'] = concepts['stand']
        #concepts['swim (V)'] = concepts['swim']
        #concepts['walk (V)'] = concepts['walk(go)']
        
        
        languages = args.writer.add_languages(
                lookup_factory="Name", id_factory=lambda x: slug(x['Name']))
        
        args.writer.add_sources()
        visited = set()
        for idx, concept in wl.iter_rows('concept'):
            if wl[idx, 'concept'] in concepts:
                lexeme = args.writer.add_form(
                        Language_ID=languages[wl[idx, 'language']],
                        Parameter_ID=concepts[wl[idx, 'concept']],
                        Value=wl[idx, 'ipa'],
                        Form='.'.join(wl[idx, 'tokens']),
                        Source='Syrjaenen2013',
                        Loan=True if wl[idx, 'cogid'] < 0 else False
                        )
                args.writer.add_cognate(
                        lexeme=lexeme,
                        Cognateset_ID=wl[idx, 'cogid'],
                        Cognate_Detection_Method='expert',
                        Source=['Syrjaenen2013']
                        )        
            else:
                if concept not in visited:
                    visited.add(concept)
                    print(concept)
