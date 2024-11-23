import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from prompts import script_writer

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.getenv("AZURE_API_VERSION")
)


def get_completion(
        prompt,
        system_role,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model=os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT"),
):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )
    return response.choices[0].message.content


def get_image(prompt):
    """returns image url"""
    response = client.images.generate(
        model=os.getenv("AZURE_OPENAI_DALLE_DEPLOYMENT"),
        prompt=prompt,
        size="1024x1024",
        quality="hd",
        n=1
    )
    return response.data[0].url


def get_speech(text, save_path, voice="echo", speed=1., response_format="mp3"):
    with client.audio.speech.with_streaming_response.create(input=text,
                                          model=os.getenv("AZURE_OPENAI_TTS_DEPLOYMENT"),
                                          voice=voice,
                                          speed=speed,
                                          response_format=response_format) as response:
        response.stream_to_file(save_path)


def get_video_script(content_data):
    return get_completion(
        prompt=script_writer.prompt+content_data,
        system_role=script_writer.system_role,
        temperature=script_writer.temperature,
        top_p=script_writer.top_p,
        frequency_penalty=script_writer.frequency_penalty,
        presence_penalty=script_writer.presence_penalty,
        model=script_writer.model,
    )


if __name__ == "__main__":
    # print(get_completion("What is the meaning of life?"))
    # print(get_image("A beautiful landscape with a sunset"))

    article_content = """ **article:** The World’s Biggest EV Maker Has the Industry’s Worst Human Rights Appraisal
Amnesty International has issued a report charting the supply chains and human rights due diligence policies of 13 major EV manufacturers. The results are a world away from the clean, safe future that electric vehicles promise.
The Worlds Biggest EV Maker Has the Industrys Worst Human Rights Appraisal
Photo-Illustration: Wired Staff/Getty

The race to keep pace with EV development could be taking a dark turn. Amnesty International has released a report claiming the world’s leading EV makers are failing to adequately demonstrate how they address human rights risks in their mineral supply chains, which gather vital materials for making electric car batteries.

The report, Recharge for Rights, alleges that BYD, Mitsubishi, and Hyundai had the worst human rights due diligence policies of 13 major EV manufacturers, ranked in a league table (the three companies did not respond to Amnesty on its findings).
Gear Newsletter: Reviews, Guides, and Deals
Upgrade your life with our buying guides, deals, and how-to guides, all tested by experts.
By signing up, you agree to our user agreement (including class action waiver and arbitration provisions), and acknowledge our privacy policy.

Other EV makers—such as Tesla, Mercedes-Benz, and Stellantis—were placed higher in Amnesty’s league table, but the organization alleges those companies could provide only a “moderate” demonstration of their human rights due diligence.

Featured Video

This Small Robotics Startup is Already Worth Billions

“The human rights abuses tied to the extraction of energy transition minerals are alarming and pervasive,” said Amnesty International’s secretary general, Agnès Callamard, lamenting in the report that the industry’s response was “sorely lacking.” Those auto companies lagging “need to work harder and faster to show that human rights isn’t just a fluff phrase, but an issue they take seriously,” she added.

When we think batteries, we think lithium mining—which already has a shaky reputation. But another key ingredient is cobalt, a significant proportion of which is mined in deep tunnels using simple tools, or even by hand. Some of the miners are children.

It is significant then that Amnesty’s report, scoring car companies not only on their appraisal of human rights but on supply chain mapping, among other factors, alleges that the largest maker of EVs globally, Chinese company BYD, is the worst offender.
Cobalt China Concern

More than two-thirds of the world’s cobalt—an essential part of lithium-ion batteries—comes from the Democratic Republic of the Congo (DRC), where there is immense poverty despite the country’s mineral wealth. Seventy percent of Congolese people live on less than $2.15 a day.

Amnesty has estimated that nearly a quarter of the cobalt sourced from DRC is from small-scale mining, where miners—including children—dig dangerously deep tunnels using simple tools or even their hands. Sourcing from other countries would take income away from these small-scale, “artisanal” miners; it’s often better for EV companies to insist on improved working conditions for all DRC miners rather than shun DRC-sourced cobalt.

Amnesty’s league table, marked out of 90, assessed car companies’ performance on criteria including commitment to human rights policies, supply chain mapping and reporting, and remediation. Mercedes-Benz scored highest with 51 out of 90. BYD—which did not disclose smelter, refiner, or mine site names to Amnesty—scored a dire 11 out of 90.
Most Popular

“[BYD’s] disclosures show a serious lack of transparency on human rights diligence in its battery supply chains,” said Amnesty’s Callamard. “Other low-scoring firms, such as Hyundai and Mitsubishi, lack the necessary depth and information about implementation across key human rights due diligence areas.”


“The commitments these companies report on are often vague and provide little evidence of meaningful action, showing they have a long way to go to meet international standards,” Callamard said.

While companies such as Renault and GM have stated their commitment to human rights due diligence, and rank higher than some of the lowest-scoring companies, they still provide limited evidence of fully integrating these commitments into their supply chain operations, with scant information about their risk assessments, according to the Recharge for Rights report.

BMW, Mercedes-Benz, Tesla, and VW have “more to do” to “identify actual and potential human rights risks across [their] supply chains,” said Amnesty, but the fact that they achieved a “moderate” score “should stand as a model for the others to follow,” stated Recharge for Rights.
Auto Compliance

Six of the 13 companies featured in the Recharge for Rights report responded to WIRED, stressing that they take the issues raised by Amnesty seriously. BMW, GM, Nissan, Mitsubishi, and Hyundai all sent statements regarding their poor scoring.

Mitsubishi said Amnesty’s report was based on information dating from 2023, “but we have initiated numerous efforts since then.” These measures, said the Japanese company, include using AI to “analyze potential connections with suppliers related to conflict minerals and other issues.”

Nissan provided WIRED with its Sustainability Data Book, which included minerals-sourcing best practices, adding that the company respected the “human rights of all stakeholders” and complied with “applicable laws, regulations, and standards.”

“Our supply chain compliance program sets out the highest standards,” stated Hyundai, adding it was “committed to a sustainable, ethical supply chain that upholds human rights, environmental protection, and safety.”

“We have been committed to respecting human rights for years, even beyond legal requirements,” Mercedes-Benz stated, highlighting that it “ranks the best among the evaluated automobile manufacturers” in Amnesty’s report.

BMW pointed WIRED to the group’s compliance management documents. General Motors said it was committed to “sustainable and responsible sourcing of goods and services.” A Ford spokesperson offered to be interviewed on a Zoom-style call but, at the agreed time, did not show up.
History of Criticism

Digging up minerals can be exceedingly lucrative for mining companies, but people who live in proximity to these resources rarely, if ever, benefit. For some Brazilian communities, this changed last month following a court case that will be keenly studied by the industries that rely on such minerals, including the automotive sector.

The largest class action in English history was filed in London on October 21, a claim involving 700,000 individuals seeking redress after a devastating tailings dam rupture in 2015 on the Doce River in southeastern Brazil. Nine years later, the Doce River—which the Krenak Indigenous people revere as a deity—is still poisoned with the iron ore mine’s deluge-related toxins.
Most Popular

Just four days after news of the lawsuit broke, the Anglo-Australian mining giant BHP entered into an compensation agreement with the country of Brazil, in which the company will pay $29.85 billion in the biggest environmental payout ever, dwarfing the $15 billion paid by VW over “Dieselgate” in 2016, and the $20.8 billion paid by BP over Deepwater Horizon in 2015.

According to reporting from Reuters, this payout could potentially resolve all current and future litigation.

Recharge for Rights is also not Amnesty’s first critique of electric car brands. In 2016, the organization released breakthrough research that alleged how leading companies were ignoring the environmental and human exploitation endemic in the extraction of the 30 metals and minerals necessary for EVs.

Working with African resources specialist Afrewatch, Amnesty documented how children as young as 8 were involved in the scouring for cobalt, and reported how conditions for both child and adult miners were exploitative and hazardous.

New regulations in Europe, the US, and Japan stipulate how companies must address human rights violations. Companies that fall foul of the new EU-wide Corporate Sustainability Due Diligence Directive—which, since July, requires strict monitoring of labor, social, and ethical conditions across companies’ supply chains—face fines of up to 5 percent of global revenue, while non-EU companies risk restricted market access.

The impact can be felt beyond the EU’s borders. “Because Chinese companies want access to Europe, the EU has a powerful leverage to say, ‘Well, if you want to come to this market, you need to meet our standards.’” says Henry Sanderson, Benchmark Mineral Intelligence executive editor and author of Volt Rush, a 2022 book that dug into automakers’ sometimes murky EV supply chains. He adds that the EU has “immense power to clean up supply chains.”

The US, via the Biden administration’s Inflation Reduction Act (IRA), is also “driving a lot of this,” says Sanderson, although more from a protectionist stance. “You can’t get some of the [IRA] credits if a so-called foreign entity of concern—a Chinese company, then—is in your supply chain,” he says. “Therefore, you need to map your supply chain.”

Supply chain mapping—the process of gathering and analyzing information about a company's supply chain to create a detailed map of its network, also known as SCM—can be a “force for good,” stressed Audi’s head of procurement strategy, Marco Philippi, to Automotive Logistics in 2022.
Most Popular


“If we have our suppliers enforce our sustainability ratings to their suppliers, we’re talking about 14,000 direct partners in 60 countries multiplied by ‘N’ acting on it,” Philippi calculated. “When we look across the group, it is 60,000 suppliers. This is a power we are aware of.”

In Recharge for Rights, Amnesty’s Callamard said: “Car companies need to use their massive leverage as global minerals buyers to influence upstream mining companies and smelters to mitigate human rights risks.”
Decarbonization Drive

Amnesty International isn’t the only civil society organization to rank automakers for their human rights compliance. The findings in Recharge for Rights echo those in recent research reports issued by Human Rights Watch and Lead the Charge, a network of local and global NGOs promoting equitable, sustainable, and fossil-free auto supply chains.

Lead the Charge found that two-thirds of the companies on its league table had no policies related to Indigenous people’s rights. The organization has called for mining companies to obtain the “free, prior, and informed consent” of Indigenous people in line with a declaration signed by Indigenous organizations at last year’s United Nations climate conference.

And what’s good for Indigenous people can often be good for the planet. A cleaner, greener auto industry can help shift heavy industries—particularly steel and aluminum—away from fossil fuels, Lead the Charge believes. The steel industry alone is responsible for 7 percent of the world’s greenhouse gas emissions. Add in aluminum and it’s more than 10 percent of all human-made emissions, says Chris Alford of the Sunrise Project, a global climate justice organization.

“The auto industry is the largest consumer of aluminum and batteries, and a top consumer of steel globally,” Alford, a Brit based in Mexico, told WIRED. “They can use this purchasing power to push other industries to decarbonize.”

Some auto companies are more eager to decarbonize than others. For instance, in 2021, Volvo announced its intentions to source fossil-free steel, and a year later became the first automaker to sign up to the SteelZero initiative, which aims to increase demand for fossil-free steel and accelerate a transition to carbon neutrality in the global steel industry. Mercedes-Benz has since made a similar commitment.
Most Popular


Like Audi head of procurement strategy Philippi, Alford believes automakers can use their purchasing power to drive the industry toward a cleaner future as it addresses environmental and human rights impacts across the car supply chain. “With EVs, we have an opportunity,” says Alford, “because the transition to electric vehicles is necessitating a transformation of auto supply chains. So, the opportunity to intervene and improve that is now, while these supply chains are already being transformed.”

Sam Hardy, the ESG lead on mining for Australian environmental consultancy JBS&G, which is not part of Lead the Charge, told WIRED that the recent Amnesty report was a “must-read if you’re interested in responsible supply chains.” Hardy states the EV brands themselves need to be acknowledged. “Rather than retreating, they have on the whole been willing to engage and work to improve sustainability approaches,” he says. “While the Amnesty scorecard still shows massive room for improvement, the sectorwide relative improvement should be praised.”

“What are the tools at our disposal to make companies respect human rights and the environment?” says Mark Dummett, head of the Amnesty team that produced Recharge for Rights. “One is pushing for laws and regulations. Another one is the work we're doing with [the Recharge for Rights] report to raise the profile of these issues. And a third tool is strategic litigation [such as the class action won against BHP] to hold companies to account. Litigation can make a difference not just in individual cases, but also in more broadly influencing corporate behavior.”

However, despite recent improvements, Dummett says he is worried about what president-elect Donald Trump’s victory in the US election could mean for the ongoing fight for human rights concerns with EV makers. “Trump has promised to weaken regulatory bodies. We’re highly concerned by that.”
You Might Also Like …


Carlton Reid is an award-winning freelancer who writes about cycling, transport and adventure travel for numerous titles including Forbes, The Guardian, and Mail Online. He is the author of Roads Were Not Built for Cars and Bike Boom."""


    reddit_comments = """ **reddit comments:** comment1: 

https://www.amnesty.org/en/documents/ACT30/8544/2024/en/

Here is the actual report in question, it is deeply stupid. This is just a measure of how much do the respective companies write statements that Amnesty likes; it doesn't have anything at all to do with the behavior of the companies.

comment2: I don’t understand , BYD cars use LFP batteries exclusively , LFP has no nickel manganese cobalt( which has some concerning environmental issues when it’s comes to extraction ) , LFP just mostly lithium and iron , the vast majority of lithium is either from Chile or Australia , so what’s the issue here ? 
comment3: t's interesting....why are reports like these simply focusing on human rights for EV and automakers? Anyone checked Apple, Amazon, ExxonMobil, banana companies, meat industry companies, coffee companies?

The entire global economy is based on human/animal rights exploitation and abuse. Everyone turns a blind eye to all of them except for the ones that suit their virtue signaling narratives. 
comment4: Nobody gave a shit about Cobalt when it was being consumed in the process of removing sulfur from oil in the refining process. Now that it's in EV batteries and is recyclable, suddenly it's the human rights issue of our time. What a fucking joke. """

    video_script = get_video_script(article_content+reddit_comments)
    print(video_script)
    get_speech(video_script, "test.mp3")