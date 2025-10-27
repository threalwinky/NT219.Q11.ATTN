from charm.toolbox.policytree import PolicyParser

class ABAC:
    attr_dict = {
        'neurology_doctor': '1',
        'dermatology_doctor': '2',
        'otorhinolaryngology_doctor':'3',
        'psychiatry_doctor':'4',
        'rheumatology_doctor':'5',
        'pharmacist': '6',
        'researcher': '7',
        'financial': '8',
        'nurse': '9',
        'patient': '10',
        'doctor': '11'
    }
    
    '''
    health_record_policy = "DOCTOR or PATIENT or nurse"
    invoice_policy = "financial"
    medicine_policy = "DOCTOR or pharmacist or PATIENT"
    research_report_policy = "(DOCTOR or researcher)"
    
    Demo policy
    '''
    
    def __init__(self):
        self.parser = PolicyParser()
    
    def check(self, attribute: list, policy: str):
        tree = self.parser.parse(policy)
        check = self.parser.prune(tree, attribute)
        
        return False if check is False else True
    
    def convertPolicy(self, policy):
        for k in self.attr_dict:
            policy = policy.replace(k, self.attr_dict[k])
        
        return policy
    
    def convertAttribute(self, attribute):
        converted_attr = []
        for a in attribute:
            for k in self.attr_dict:
                if a == k:
                    converted_attr.append(self.attr_dict[k])
        
        return converted_attr
    

def checker(user_attr, POLICY):
    final_attr = []
    final_policy = []

    final_attr = [p for p in POLICY if any(p in p2 for p2 in user_attr)]        
    final_policy = list(set(final_policy + [p2 for p in POLICY for p2 in final_attr if p in p2] + POLICY))
    
    abac = ABAC()

    pol = abac.convertPolicy(' or '.join(final_policy))
    attr = abac.convertAttribute(final_attr)

    if not abac.check(attr, pol):
        return False
    return True